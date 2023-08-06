
import logging
import os
from datetime import datetime
import numbers
import re
import numpy as np
import pandas as pd
from sklearn import model_selection, tree, ensemble, svm, linear_model, neighbors, metrics
from sklearn.model_selection import GroupKFold, StratifiedKFold
from sklearn.metrics.pairwise import cosine_similarity
from joblib import dump, load
import pkg_resources
from openpredict.rdf_utils import add_run_metadata, retrieve_features, add_feature_metadata
# from openpredict.openpredict_utils import get_spark_context
# from openpredict.openpredict_utils import get_spark_context
from openpredict.openpredict_utils import get_openpredict_dir, get_entities_labels

# models_folder = 'openpredict/data/models/'

hyper_params = {
    'penalty': 'l2',
    'dual': False,
    'tol': 0.0001,
    'C': 1.0,
    'random_state': 100
}

def get_spark_context():
    """Get Spark context, either from Spark Master URL to a Spark cluster
    If not URL is provided, then it will try to run Spark locally 

    :return: Spark context
    """
    spark_master_url = os.getenv('SPARK_MASTER_URL')

    sc = None
    if os.getenv('SPARK_HOME'):
        # Do not try to run Spark if SPARK_HOME env variable not set
        logging.info('SPARK env var found')
        # import findspark
        # findspark.init(os.getenv('SPARK_HOME'))
        import pyspark
        if spark_master_url:
            logging.info('SPARK_MASTER_URL provided, connecting to the Spark cluster ✨')
            # e.g. spark://my-spark-spark-master:7077
            sc = pyspark.SparkContext(appName="Pi", master=spark_master_url)
            logging.info(sc)
        else:
            try:
                logging.info('SPARK_MASTER_URL not provided, trying to start Spark locally ✨')
                sc = pyspark.SparkContext.getOrCreate()
                logging.info(sc)
            except:
                logging.info("Could not start a Spark cluster locally. Using pandas to handle dataframes 🐼")
    else:
        logging.info('SPARK_HOME not found, using pandas to handle dataframes 🐼')
    return sc
    ## Old way:
    #     import findspark
    #     from pyspark import SparkConf, SparkContext
    #     findspark.init()

    #     config = SparkConf()
    #     config.setMaster("local[*]")
    #     config.set("spark.executor.memory", "5g")
    #     config.set('spark.driver.memory', '5g')
    #     config.set("spark.memory.offHeap.enabled",True)
    #     config.set("spark.memory.offHeap.size","5g") 
    #     sc = SparkContext(conf=config, appName="OpenPredict")

def adjcencydict2matrix(df, name1, name2):
    """Convert dict to matrix

    :param df: Dataframe
    :param name1: index name
    :param name2: columns name
    """
    df1 = df.copy()
    df1= df1.rename(index=str, columns={name1: name2, name2: name1})
    print('📏 Dataframe size')
    print(len(df))
    df =df.append(df1)
    print(len(df))
    print(len(df))
    return df.pivot(index=name1, columns=name2)


def addEmbedding(embedding_file, emb_name, types, description, from_model_id):
    """Add embedding to the drug similarity matrix dataframe

    :param embedding_file: JSON file containing records ('entity': id, 'embdding': array of numbers )
    :param emb_name: new column name to be added
    :param types: types in the embedding vector ['Drugs', 'Diseases', 'Both']
    :param description: description of the embedding provenance
    """
    emb_df = pd.read_json(embedding_file, orient='records') 
    #emb_df = pd.read_csv(embedding_file) 
    emb_df.entity= emb_df.entity.str.replace('DRUGBANK:','')
    #print (emb_df.head())
    emb_df.set_index('entity',inplace=True) 
    
    print (emb_df.head())
    emb_size = len(emb_df.iloc[0]['embedding'])
    print ('Embedding dimension',emb_size)

    # TODO: now also save the feature dataframe for each run to be able to add embedding to any run?
    # Or can we just use the models/run_id.joblib file instead of having 2 files for 1 run?
    print('📥 Loading features file: ' + get_openpredict_dir('features/' + from_model_id + '.joblib'))
    (drug_df, disease_df)= load(get_openpredict_dir('features/' + from_model_id + '.joblib'))

    if  types == 'Drugs':
        names = drug_df.columns.levels[1]
        header = ["Drug1", "Drug2", emb_name]
    else:
        names = disease_df.columns.levels[1]
        header = ["Disease1", "Disease2", emb_name]

    entity_exist = [ d for d in names if d in emb_df.index]
    print ("Number of drugs that do not exist in the embedding ", len(names)- len(entity_exist))
    # Copy only drug entity embeddings 
    embedding_df = emb_df.loc[entity_exist].copy()
    emb_matrix = np.empty(shape=(0, emb_size))
    for d in names:
        # add zeros values for drugs that do not exist in the embedding
        if d not in emb_df.index:
            emb_matrix= np.vstack([emb_matrix, np.zeros(emb_size)])
        else:
            emb_matrix= np.vstack([emb_matrix, np.array(embedding_df.loc[d]['embedding'])])
    # calculate cosine similarity for given embedding
    sim_mat =cosine_similarity(emb_matrix, emb_matrix)
    # convert to DF
    df_sim = pd.DataFrame(sim_mat, index = names, columns=names)
    # if there is NA (It is the case when both pairs have zero values-no embedding exist)
    df_sim = df_sim.fillna(0.0)
    # make multi-index dataframe adding a new column with given embedding name
    df_sim_m = pd.concat([df_sim], axis=1, keys=[emb_name])
    # finally concatenate the embedding-based similarity to other drug similarity matrix
    print (df_sim_m.sample(5))

    # add to the similarity tensor

    if types =="Drugs":
        drug_df= pd.concat([drug_df, df_sim_m],  axis=1)
    elif types == "Diseases":
        disease_df= pd.concat([disease_df, df_sim_m],  axis=1)  

    add_feature_metadata(emb_name, description, types)
    # train the model again
    clf, scores, hyper_params = train_model(from_model_id)

     # TODO: How can we get the list of features directly from the built model?
    # The baseline features are here, but not the one added 
    # drug_features_df = drug_df.columns.get_level_values(0).drop_duplicates()
    # disease_features_df = disease_df.columns.get_level_values(0).drop_duplicates()
    # model_features = drug_features_df.values.tolist() + disease_features_df.values.tolist()
    model_features = retrieve_features('All').keys()

    run_id = add_run_metadata(scores, model_features, hyper_params)

    # dump((drug_df, disease_df), 'openpredict/data/features/drug_disease_dataframes.joblib')
    dump((drug_df, disease_df), get_openpredict_dir('features/' + run_id + '.joblib'))
    print ('New embedding based similarity was added to the similarity tensor and dataframes with new features are store in data/features/' + run_id + '.joblib')

    dump(clf, get_openpredict_dir('models/' + run_id + '.joblib'))
    print('\nStore the model in the file ' + get_openpredict_dir('models/' + run_id) + '.joblib 💾')
    # See skikit docs: https://scikit-learn.org/stable/modules/model_persistence.html

    #df_sim_m= df_sim.stack().reset_index(level=[0,1])
    #df_sim_m.to_csv(pkg_resources.resource_filename('openpredict', os.path.join("data/features/", emb_name+'.csv')), header=header)
    return run_id 


def mergeFeatureMatrix(drugfeatfiles, diseasefeatfiles):
    """Merge the drug and disease feature matrix

    :param drugfeatfiles: Drug features files list
    :param diseasefeatfiles: Disease features files list
    """
    print('Load and merge features files 📂')
    drug_df = None
    for i,featureFilename in enumerate(drugfeatfiles):
        print(featureFilename)
        df = pd.read_csv(featureFilename, delimiter=',')
        print (df.columns)
        cond = df.Drug1 > df.Drug2
        df.loc[cond, ['Drug1', 'Drug2']] = df.loc[cond, ['Drug2', 'Drug1']].values
        if i != 0:
            drug_df=drug_df.merge(df,on=['Drug1','Drug2'],how='inner')
            #drug_df=drug_df.merge(temp,how='outer',on='Drug')
        else:
            drug_df=df
    drug_df.fillna(0, inplace=True)
    
    drug_df = adjcencydict2matrix(drug_df, 'Drug1', 'Drug2')
    drug_df = drug_df.fillna(1.0)

    disease_df = None
    for i,featureFilename in enumerate(diseasefeatfiles):
        print(featureFilename)
        df=pd.read_csv(featureFilename, delimiter=',')
        cond = df.Disease1 > df.Disease2
        df.loc[cond, ['Disease1','Disease2']] = df.loc[cond, ['Disease2','Disease1']].values
        if i != 0:
            disease_df = disease_df.merge(df,on=['Disease1','Disease2'], how='inner')
            #drug_df=drug_df.merge(temp,how='outer',on='Drug')
        else:
            disease_df = df
    disease_df.fillna(0, inplace=True)
    disease_df.Disease1 = disease_df.Disease1.astype(str)
    disease_df.Disease2 = disease_df.Disease2.astype(str)
    
    disease_df = adjcencydict2matrix(disease_df, 'Disease1', 'Disease2')
    disease_df = disease_df.fillna(1.0)
    
    return drug_df, disease_df


def generatePairs(drug_df, disease_df, drugDiseaseKnown):
    """Generate positive and negative pairs using the Drug dataframe, 
    the Disease dataframe and known drug-disease associations dataframe 

    :param drug_df: Drug dataframe
    :param disease_df: Disease dataframe
    :param drugDiseaseKnown: Known drug-disease association dataframe
    """
    drugwithfeatures = set(drug_df.columns.levels[1])
    diseaseswithfeatures = set(disease_df.columns.levels[1])
    
    drugDiseaseDict  = set([tuple(x) for x in  drugDiseaseKnown[['Drug','Disease']].values])

    commonDrugs= drugwithfeatures.intersection( drugDiseaseKnown.Drug.unique())
    commonDiseases=  diseaseswithfeatures.intersection(drugDiseaseKnown.Disease.unique() )
    print("💊 commonDrugs: %d 🦠  commonDiseases: %d"%(len(commonDrugs),len(commonDiseases)))

    #abridged_drug_disease = [(dr,di)  for  (dr,di)  in drugDiseaseDict if dr in drugwithfeatures and di in diseaseswithfeatures ]

    #commonDrugs = set( [ dr  for dr,di in  abridged_drug_disease])
    #commonDiseases  =set([ di  for dr,di in  abridged_drug_disease])

    print("\n🥇 Gold standard, associations: %d drugs: %d diseases: %d"%(len(drugDiseaseKnown),len(drugDiseaseKnown.Drug.unique()),len(drugDiseaseKnown.Disease.unique())))
    print("\n🏷️  Drugs with features  : %d Diseases with features: %d"%(len(drugwithfeatures),len(diseaseswithfeatures)))
    print("\n♻️  commonDrugs : %d commonDiseases : %d"%(len(commonDrugs),len(commonDiseases)))

    pairs=[]
    classes=[]
    for dr in commonDrugs:
        for di in commonDiseases:
            cls = (1 if (dr,di) in drugDiseaseDict else 0)
            pairs.append((dr,di))
            classes.append(cls)
            
    return pairs, classes


def balance_data(pairs, classes, n_proportion):
    """Balance negative and positives samples

    :param pairs: Positive/negative pairs previously generated
    :param classes: Classes corresponding to the pairs
    :param n_proportion: Proportion number, e.g. 2
    """
    classes = np.array(classes)
    pairs = np.array(pairs)
    
    indices_true = np.where(classes == 1)[0]
    indices_false = np.where(classes == 0)[0]

    np.random.shuffle(indices_false)
    indices = indices_false[:(n_proportion*indices_true.shape[0])]
    print("\n⚖️  ➕/➖ :", len(indices_true), len(indices), len(indices_false))
    pairs = np.concatenate((pairs[indices_true], pairs[indices]), axis=0)
    classes = np.concatenate((classes[indices_true], classes[indices]), axis=0) 
    
    return pairs, classes


def geometricMean(drug, disease, knownDrugDisease, drugDF, diseaseDF):
    """Compute the geometric means of a drug-disease association using previously generated dataframes

    :param drug: Drug
    :param disease: Disease
    :param knownDrugDisease: Known drug-disease associations
    :param drugDF: Drug dataframe
    :param diseaseDF: Disease dataframe
    """
    a  = drugDF.loc[knownDrugDisease[:,0]][drug].values
    b  = diseaseDF.loc[knownDrugDisease[:,1]][disease].values
    c = np.sqrt( np.multiply(a,b) )
    ix2 = (knownDrugDisease == [drug, disease])
    c[ix2[:,1]& ix2[:,0]]=0.0
    return float(max(c))


def createFeatureArray(drug, disease, knownDrugDisease, drugDFs, diseaseDFs):
    """Create the features dataframes for Spark.

    :param drug: Drug
    :param disease: Disease
    :param knownDrugDisease: Known drug-disease associations
    :param drugDFs: Drug dataframes
    :param diseaseDFs: Disease dataframes
    :return: The features dataframe 
    """
    #featureMatri x= np.empty((len(classes),totalNumFeatures), float)
    feature_array =[]
    for i,drug_col in enumerate(drugDFs.columns.levels[0]):
        for j,disease_col in enumerate(diseaseDFs.columns.levels[0]):
            drugDF = drugDFs[drug_col]
            diseaseDF = diseaseDFs[disease_col]
            feature_array.append( geometricMean( drug, disease, knownDrugDisease, drugDF, diseaseDF))
            #print (feature_series) 
    return feature_array


def sparkBuildFeatures(sc, pairs, classes, knownDrugDis,  drug_df, disease_df):
    """Create the feature matrix for Spark.

    :param sc: Spark context
    :param pairs: Generated pairs
    :param classes: Classes corresponding to the pairs
    :param knownDrugDisease: Known drug-disease associations
    :param drugDFs: Drug dataframes
    :param diseaseDFs: Disease dataframes
    :return: The features dataframe 
    """

    rdd = sc.parallelize(list(zip(pairs[:,0], pairs[:,1], classes))).map(lambda x: (x[0],x[1],x[2], createFeatureArray( x[0], x[1], knownDrugDis,  drug_df, disease_df)))
    all_scores = rdd.collect()
    drug_col = drug_df.columns.levels[0]
    disease_col = disease_df.columns.levels[0]
    combined_features = ['Feature_'+dr_col+'_'+di_col for dr_col in drug_col  for di_col in disease_col]
    a = [ e[0] for e in all_scores]
    b = [ e[1] for e in all_scores]
    c = [ e[2] for e in all_scores]
    scores = [ e[3] for e in all_scores]
    df = pd.DataFrame(scores, columns=combined_features)
    df['Drug'] = a
    df['Disease' ] = b 
    df['Class' ] = c 
    return df



def createFeatureDF(pairs, classes, knownDrugDisease, drugDFs, diseaseDFs):
    """Create the features dataframes.

    :param pairs: Generated pairs
    :param classes: Classes corresponding to the pairs
    :param knownDrugDisease: Known drug-disease associations
    :param drugDFs: Drug dataframes
    :param diseaseDFs: Disease dataframes
    :return: The features dataframe 
    """
    totalNumFeatures = len(drugDFs)*len(diseaseDFs)
    #featureMatri x= np.empty((len(classes),totalNumFeatures), float)
    df =pd.DataFrame(list(zip(pairs[:,0], pairs[:,1], classes)), columns =['Drug','Disease','Class'])
    index = 0
    for i,drug_col in enumerate(drugDFs.columns.levels[0]):
        for j,disease_col in enumerate(diseaseDFs.columns.levels[0]):
            drugDF = drugDFs[drug_col]
            diseaseDF = diseaseDFs[disease_col]
            feature_series = df.apply(lambda row: geometricMean( row.Drug, row.Disease, knownDrugDisease, drugDF, diseaseDF), axis=1)
            #print (feature_series) 
            df["Feature_"+str(drug_col)+'_'+str(disease_col)] = feature_series
    return df


def calculateCombinedSimilarity(pairs_train, pairs_test, classes_train, classes_test, drug_df, disease_df, knownDrugDisease):
    """Compute combined similarities. Use Spark if available for speed, otherwise use pandas

    :param pairs_train: Pairs used to train
    :param pairs_test: Pairs used to test
    :param classes_train: Classes corresponding to the pairs used to train
    :param classes_test: Classes corresponding to the pairs used to test
    :param drug_df: Drug dataframe
    :param disease_df: Disease dataframe
    :param knownDrugDisease: Known drug-disease associations
    """
    spark_context = get_spark_context()
    if spark_context:
        drug_df_bc= spark_context.broadcast(drug_df)
        disease_df_bc = spark_context.broadcast(disease_df)
        knownDrugDis_bc = spark_context.broadcast(knownDrugDisease)
        logging.info('Running Spark ✨')
       
        train_df= sparkBuildFeatures(spark_context, pairs_train, classes_train, knownDrugDis_bc.value,  drug_df_bc.value, disease_df_bc.value)
        test_df= sparkBuildFeatures(spark_context, pairs_test, classes_test, knownDrugDis_bc.value,  drug_df_bc.value, disease_df_bc.value)
        logging.info("Finishing Spark jobs 🏁")
    else:
        logging.info("Spark cluster not found, using pandas 🐼")
        train_df  = createFeatureDF(pairs_train, classes_train, knownDrugDisease, drug_df, disease_df)
        test_df = createFeatureDF(pairs_test, classes_test, knownDrugDisease, drug_df, disease_df)
    
    return train_df, test_df


def train_classifier(train_df, clf):
    """Train classifier
    
    :param train_df: Train dataframe
    :param clf: Classifier
    """
    features = list(train_df.columns.difference(['Drug','Disease','Class']))
    X = train_df[features]
    print("Dataframe sample of training X (train_classifier features):")
    print(X.head())
    y = train_df['Class']
    print(y.head())
    print('📦 Fitting classifier...')
    clf.fit(X, y)
    return clf

def multimetric_score(estimator, X_test, y_test, scorers):
    """Return a dict of score for multimetric scoring
    
    :param estimator: Estimator
    :param X_test: X test
    :param y_test: Y test
    :param scorers: Dict of scorers
    :return: Multimetric scores
    """
    scores = {}
    for name, scorer in scorers.items():
        if y_test is None:
            score = scorer(estimator, X_test)
        else:
            score = scorer(estimator, X_test, y_test)

        if hasattr(score, 'item'):
            try:
                # e.g. unwrap memmapped scalars
                score = score.item()
            except ValueError:
                # non-scalar?
                pass
        scores[name] = score

        if not isinstance(score, numbers.Number):
            raise ValueError("scoring must return a number, got %s (%s) "
                             "instead. (scorer=%s)"
                             % (str(score), type(score), name))
    return scores

def evaluate(test_df, clf):
    """Evaluate the trained classifier
    :param test_df: Test dataframe
    :param clf: Classifier
    :return: Scores
    """
    features = list(test_df.columns.difference(['Drug','Disease','Class']))
    X_test =  test_df[features]
    y_test = test_df['Class']

    # https://scikit-learn.org/stable/modules/model_evaluation.html#using-multiple-metric-evaluation
    scoring = ['precision', 'recall', 'accuracy', 'roc_auc', 'f1', 'average_precision']
    
    # TODO: check changes here
    # scorers, multimetric = metrics.scorer._check_multimetric_scoring(clf, scoring=scoring)
    # AttributeError: module 'sklearn.metrics' has no attribute 'scorer'
    # scorers, multimetric = metrics.get_scorer._check_multimetric_scoring(clf, scoring=scoring)
    # AttributeError: 'function' object has no attribute '_check_multimetric_scoring'
    scorers = {}
    for scorer in scoring:
        scorers[scorer] = metrics.get_scorer(scorer)
    
    scores = multimetric_score(clf, X_test, y_test, scorers)
    return scores

def createFeaturesSparkOrDF(pairs, classes, drug_df, disease_df):
    """Create features dataframes. Use Spark if available for speed, otherwise use pandas
    :param pairs: pairs
    :param classes: classes
    :param drug_df: drug 
    :param disease_df: disease dataframe
    :return: Feature dataframe
    """
    spark_context = get_spark_context()
    if spark_context:
        logging.info('Running Spark ✨')
        drug_df_bc= spark_context.broadcast(drug_df)
        disease_df_bc = spark_context.broadcast(disease_df)
        knownDrugDis_bc = spark_context.broadcast(pairs[classes==1])
        feature_df= sparkBuildFeatures(spark_context, pairs, classes, knownDrugDis_bc.value,  drug_df_bc.value, disease_df_bc.value)
        logging.info("Finishing Spark jobs 🏁")
    else:
        logging.info("Spark cluster not found, using pandas 🐼")
        feature_df = createFeatureDF(pairs, classes, pairs[classes==1], drug_df, disease_df)
    return feature_df


def train_model(from_model_id='openpredict-baseline-omim-drugbank'):
    """The main function to run the drug-disease similarities pipeline, 
    and train the drug-disease classifier.
    It returns, and stores the generated classifier as a `.joblib` file 
    in the `data/models` folder,
    
    :param from_scratch: Train the model for scratch (True by default)
    :return: Classifier of predicted similarities and scores
    """
    time_start = datetime.now()
    baseline_features_folder = "data/baseline_features/"
    drugfeatfiles = ['drugs-fingerprint-sim.csv','drugs-se-sim.csv', 
                     'drugs-ppi-sim.csv', 'drugs-target-go-sim.csv','drugs-target-seq-sim.csv']
    diseasefeatfiles =['diseases-hpo-sim.csv',  'diseases-pheno-sim.csv' ]
    drugfeatfiles = [ pkg_resources.resource_filename('openpredict', os.path.join(baseline_features_folder, fn)) for fn in drugfeatfiles]
    diseasefeatfiles = [ pkg_resources.resource_filename('openpredict', os.path.join(baseline_features_folder, fn)) for fn in diseasefeatfiles]

    # Prepare drug-disease dictionary
    drugDiseaseKnown = pd.read_csv(pkg_resources.resource_filename('openpredict', 'data/resources/openpredict-omim-drug.csv'),delimiter=',') 
    drugDiseaseKnown.rename(columns={'drugid':'Drug','omimid':'Disease'}, inplace=True)
    drugDiseaseKnown.Disease = drugDiseaseKnown.Disease.astype(str)
    # print(drugDiseaseKnown.head())

    print ("📥 Loading the similarity tensor from " + get_openpredict_dir('features/' + from_model_id + '.joblib'))
    (drug_df, disease_df)= load(get_openpredict_dir('features/' + from_model_id + '.joblib'))
    
    # Merge feature matrix to start from scratch
    # drug_df, disease_df = mergeFeatureMatrix(drugfeatfiles, diseasefeatfiles)
    # dump((drug_df, disease_df), 'openpredict/data/features/openpredict-baseline-omim-drugbank.joblib')

    print ("Drug Features ",drug_df.columns.levels[0])
    print ("Disease Features ",disease_df.columns.levels[0])
    # Generate positive and negative pairs
    pairs, classes = generatePairs(drug_df, disease_df, drugDiseaseKnown)

    # Balance negative/positive samples
    n_proportion = 2
    print("\n🍱 n_proportion: " + str(n_proportion))
    pairs, classes= balance_data(pairs, classes, n_proportion)

    # Train-Test Splitting
    pairs_train, pairs_test, classes_train, classes_test = model_selection.train_test_split(pairs, classes, stratify=classes, test_size=0.2, shuffle=True)
    # print(len(pairs_train), len(pairs_test))

    # Feature extraction (Best Combined similarity)
    print('\nFeature extraction ⛏️')
    knownDrugDisease = pairs_train[classes_train==1]
    time_pairs_train = datetime.now()

    print('Pairs train runtime 🕓  ' + str(time_pairs_train - time_start))
    print('\nCalculate the combined similarity of the training pairs 🏳️‍🌈')
    train_df, test_df = calculateCombinedSimilarity(pairs_train, pairs_test, classes_train, classes_test, drug_df, disease_df, knownDrugDisease)
    time_calculate_similarity = datetime.now()
    print('CalculateCombinedSimilarity runtime 🕓  ' + str(time_calculate_similarity - time_pairs_train))

    # Model Training, get classifier (clf)
    print('\nModel training, getting the classifier 🏃')
    clf = linear_model.LogisticRegression(penalty=hyper_params['penalty'],
            dual=hyper_params['dual'], tol=hyper_params['tol'], 
            C=hyper_params['C'], random_state=hyper_params['random_state']) 
    clf = train_classifier(train_df, clf)
    time_training = datetime.now()
    print('Model training runtime 🕕  ' + str(time_training - time_calculate_similarity))

    # Evaluation of the trained model
    print('\nRunning evaluation of the model 📝')
    scores = evaluate(test_df, clf)
    time_evaluate = datetime.now()
    print('Evaluation runtime 🕗  ' + str(time_evaluate - time_training))

    # About 3min to run on a laptop
    print("\nTest results 🏆")
    print(scores)

    print("\n Train the final model using all dataset")
    final_training = datetime.now()
    train_df = createFeaturesSparkOrDF(pairs, classes, drug_df, disease_df)

    clf = linear_model.LogisticRegression(penalty=hyper_params['penalty'],
            dual=hyper_params['dual'], tol=hyper_params['tol'], 
            C=hyper_params['C'], random_state=hyper_params['random_state']) 
    # penalty: HyperParameter , l2: HyperParameterSetting
    # Implementation: LogisticRegression
    clf = train_classifier(train_df, clf)
    print('Final model training runtime 🕕  ' + str(datetime.now() - final_training))

    # print('\nStore the model in a .joblib file 💾')
    # dump(clf, models_folder + 'openpredict-baseline-omim-drugbank.joblib')
    # See skikit docs: https://scikit-learn.org/stable/modules/model_persistence.html

    print('Complete runtime 🕛  ' + str(datetime.now() - time_start))
    return clf, scores, hyper_params


def query_omim_drugbank_classifier(input_curie, model_id):
    """The main function to query the drug-disease OpenPredict classifier, 
    It queries the previously generated classifier a `.joblib` file 
    in the `data/models` folder
    
    :return: Predictions and scores
    """
    
    parsed_curie = re.search('(.*?):(.*)', input_curie)
    input_namespace = parsed_curie.group(1)
    input_id = parsed_curie.group(2)

    # resources_folder = "data/resources/"
    #features_folder = "data/features/"
    #drugfeatfiles = ['drugs-fingerprint-sim.csv','drugs-se-sim.csv', 
    #                 'drugs-ppi-sim.csv', 'drugs-target-go-sim.csv','drugs-target-seq-sim.csv']
    #diseasefeatfiles =['diseases-hpo-sim.csv',  'diseases-pheno-sim.csv' ]
    #drugfeatfiles = [ os.path.join(features_folder, fn) for fn in drugfeatfiles]
    #diseasefeatfiles = [ os.path.join(features_folder, fn) for fn in diseasefeatfiles]

    ## Get all DFs
    # Merge feature matrix
    #drug_df, disease_df = mergeFeatureMatrix(drugfeatfiles, diseasefeatfiles)
    # (drug_df, disease_df)= load('data/features/drug_disease_dataframes.joblib')

    print("📥 Loading features " + get_openpredict_dir('features/' + model_id + '.joblib'))
    (drug_df, disease_df)= load(get_openpredict_dir('features/' + model_id + '.joblib'))

    # TODO: should we update this file too when we create new runs?
    drugDiseaseKnown = pd.read_csv(pkg_resources.resource_filename('openpredict', 'data/resources/openpredict-omim-drug.csv'),delimiter=',') 
    drugDiseaseKnown.rename(columns={'drugid':'Drug','omimid':'Disease'}, inplace=True)
    drugDiseaseKnown.Disease = drugDiseaseKnown.Disease.astype(str)

    # TODO: save json?
    drugDiseaseDict  = set([tuple(x) for x in  drugDiseaseKnown[['Drug','Disease']].values])

    drugwithfeatures = set(drug_df.columns.levels[1].tolist())
    diseaseswithfeatures = set(disease_df.columns.levels[1].tolist())

    # TODO: save json?
    commonDrugs= drugwithfeatures.intersection( drugDiseaseKnown.Drug.unique())
    commonDiseases=  diseaseswithfeatures.intersection(drugDiseaseKnown.Disease.unique() )

    # clf = load('data/models/openpredict-baseline-omim-drugbank.joblib') 
    print("📥 Loading classifier " + get_openpredict_dir('models/' + model_id + '.joblib'))
    clf = load(get_openpredict_dir('models/' + model_id + '.joblib'))

    pairs=[]
    classes=[]
    if input_namespace.lower() == "drugbank":
        # Input is a drug, we only iterate on disease
        dr = input_id
        # drug_column_label = "source"
        # disease_column_label = "target"
        for di in commonDiseases:
            cls = (1 if (dr,di) in drugDiseaseDict else 0)
            pairs.append((dr,di))
            classes.append(cls)
    else: 
        # Input is a disease
        di = input_id
        # drug_column_label = "target"
        # disease_column_label = "source"
        for dr in commonDrugs:
            cls = (1 if (dr,di) in drugDiseaseDict else 0)
            pairs.append((dr,di))
            classes.append(cls)

    classes = np.array(classes)
    pairs = np.array(pairs)

    test_df = createFeaturesSparkOrDF(pairs, classes, drug_df, disease_df)
    
    # Get list of drug-disease pairs (should be saved somewhere from previous computer?)
    # Another API: given the type, what kind of entities exists?
    # Getting list of Drugs and Diseases:
    # commonDrugs= drugwithfeatures.intersection( drugDiseaseKnown.Drug.unique())
    # commonDiseases=  diseaseswithfeatures.intersection(drugDiseaseKnown.Disease.unique() )
    features = list(test_df.columns.difference(['Drug','Disease','Class']))
    y_proba = clf.predict_proba(test_df[features])

    prediction_df = pd.DataFrame( list(zip(pairs[:,0], pairs[:,1], y_proba[:,1])), columns =['drug','disease','score'])
    prediction_df.sort_values(by='score', inplace=True, ascending=False)
    # prediction_df = pd.DataFrame( list(zip(pairs[:,0], pairs[:,1], y_proba[:,1])), columns =[drug_column_label,disease_column_label,'score'])
    
    # Add namespace to get CURIEs from IDs
    prediction_df["drug"]= "DRUGBANK:" + prediction_df["drug"]
    prediction_df["disease"] ="OMIM:" + prediction_df["disease"]

    # prediction_results=prediction_df.to_json(orient='records')
    prediction_results=prediction_df.to_dict(orient='records')
    return prediction_results

def get_predictions(id_to_predict, model_id, min_score=None, max_score=None, n_results=None):
    """Run classifiers to get predictions

    :param id_to_predict: Id of the entity to get prediction from
    :param classifier: classifier used to get the predictions
    :param score: score minimum of predictions
    :param n_results: number of predictions to return
    :return: predictions in array of JSON object
    """
    # classifier: Predict OMIM-DrugBank
    # TODO: improve when we will have more classifier
    predictions_array = query_omim_drugbank_classifier(id_to_predict, model_id)
    
    if min_score:
        predictions_array = [p for p in predictions_array if p['score'] >= min_score]
    if max_score:
        predictions_array = [p for p in predictions_array if p['score'] <= max_score]
    if n_results:
        # Predictions are already sorted from higher score to lower
        predictions_array = predictions_array[:n_results]
    
    # Build lists of unique node IDs to retrieve label
    predicted_ids = set([])
    for prediction in predictions_array:
        for key, value in prediction.items():
            if key != 'score':
                predicted_ids.add(value)
    labels_dict = get_entities_labels(predicted_ids)

    # TODO: format using a model similar to BioThings:
    # cf. at the end of this file

    # Add label for each ID, and reformat the dict using source/target
    labelled_predictions = []
    # Second array with source and target info for the reasoner query resolution
    source_target_predictions = []
    for prediction in predictions_array:
        labelled_prediction = {}
        source_target_prediction = {}
        for key, value in prediction.items():
            if key == 'score':
                labelled_prediction['score'] = value
                source_target_prediction['score'] = value
            elif value == id_to_predict:
                # Only for the source_target_prediction object
                source_target_prediction['source'] = {
                    'id': id_to_predict,
                    'type': key
                }
                try:
                    if id_to_predict in labels_dict and labels_dict[id_to_predict] and labels_dict[id_to_predict]['id'] and labels_dict[value]['id']['label']:
                        source_target_prediction['source']['label'] = labels_dict[id_to_predict]['id']['label']
                except:
                    print('No label found for ' + value)
            else:
                labelled_prediction['id'] = value
                labelled_prediction['type'] = key
                # Same for source_target object
                source_target_prediction['target'] = {
                    'id': value,
                    'type': key
                }
                try:
                    if value in labels_dict and labels_dict[value]:
                        labelled_prediction['label'] = labels_dict[value]['id']['label']
                        source_target_prediction['target']['label'] = labels_dict[value]['id']['label']
                except:
                    print('No label found for ' + value)
                # if value in labels_dict and labels_dict[value] and labels_dict[value]['id'] and labels_dict[value]['id']['label']:
                #     labelled_prediction['label'] = labels_dict[value]['id']['label']
                #     source_target_prediction['target']['label'] = labels_dict[value]['id']['label']

        labelled_predictions.append(labelled_prediction)
        source_target_predictions.append(source_target_prediction)
        # returns
        # { score: 12,
        #  source: {
        #      id: DB0001
        #      type: drug,
        #      label: a drug
        #  },
        #  target { .... }}
    
    return labelled_predictions, source_target_predictions


    # {
    # "took": 1,
    # "total": 4,
    # "max_score": 12.203629,
    # "hits": [
    #     {
    #     "@type": "Gene",
    #     "_id": "C0212166",
    #     "_score": 12.203629,
    #     "has_part": [
    #         {
    #         "@type": "ChemicalSubstance",
    #         "name": "DNA",
    #         "pmid": [
    #             "7553674"
    #         ],
    #         "umls": "C0012854"
    #         }
    #     ],
    #     "located_in": [
    #         {
    #         "@type": "AnatomicalEntity",
    #         "name": "Plasma",
    #         "pmid": [
    #             "1473120"
    #         ],
    #         "umls": "C0032105"
    #         },
    #         {
    #         "@type": "Cell",
    #         "name": "Tumor cells, malignant",
    #         "pmid": [
    #             "7691406"
    #         ],
    #         "umls": "C0334227"
    #         }
    #     ],
    #     "name": "cancer-recognition, immunedefense suppression, serine protease protection peptide",
    #     "part_of": [
    #         {
    #         "@type": "Cell",
    #         "name": "Lymphocyte",
    #         "pmid": [
    #             "7691405"
    #         ],
    #         "umls": "C0024264"
    #         }
    #     ],
    #     "physically_interacts_with": [
    #         {
    #         "@type": "Gene",
    #         "name": "Serine Endopeptidases",
    #         "pmid": [
    #             "7691406"
    #         ],
    #         "umls": "C0036734"
    #         }
    #     ],
    #     "umls": "C0212166"
    #     },