from pyspark.sql import SparkSession
from pyspark.ml.feature import StringIndexer # Perform encoding
from pyspark.ml.classification import MultilayerPerceptronClassifier
from pyspark.ml.feature import Tokenizer, StopWordsRemover, CountVectorizer
from pyspark.sql import functions as F
from pyspark.sql.functions import when
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.ml.classification import MultilayerPerceptronClassificationModel


#Create a Spark session
spark = SparkSession.builder \
    .appName("NeuralNetwork") \
    .getOrCreate()

spark

# Loading the dataset into a Spark DataFrame
# 5572 rows
data = spark.read.csv("email.csv", header=True, inferSchema=True) #dataset is taken from kaggle.com "Spam email classification"


#Output dataframe values using show() method
# We will classify whether the message is a spam or not.
data.show()


# Create a StringIndexer to encode the "Category" column
category_index = StringIndexer(inputCol="Category", outputCol="CategoryIndex")

# Apply the StringIndexer to the DataFrame
data_df = category_index.fit(data).transform(data)

data_df.show() # returns 1 if it is a spam, or zero if it is a ham (email is legitimate)



# Choosing a different output column name for the Tokenizer transformation
tokenizer = Tokenizer(inputCol="Message", outputCol="message_tokens")
data_df = tokenizer.transform(data_df)

# Lowercasing
data_df = data_df.withColumn("message_tokens_lower", F.expr("transform(message_tokens, x -> lower(x))"))

# Removing Punctuation and Special Characters (assuming "message_tokens_lower" is the column after lowercasing)
data_df = data_df.withColumn("message_tokens_clean", F.expr("transform(message_tokens_lower, x -> regexp_replace(x, '[^a-zA-Z\\s]', ''))"))

# Removing Stopwords
remover = StopWordsRemover(inputCol="message_tokens_clean", outputCol="message_tokens_filtered")
data_df = remover.transform(data_df)

# Vectorization (using CountVectorizer)
vectorizer = CountVectorizer(inputCol="message_tokens_filtered", outputCol="features")
model = vectorizer.fit(data_df)
data_df = model.transform(data_df)

# Drop intermediate columns
data_df = data_df.drop("message_tokens", "message_tokens_lower", "message_tokens_clean", "message_tokens_filtered")

# Show the transformed DataFrame
data_df.show(5)


#We create a training and test dataset. 80% of the data is for training, the rest is for testing. Seed - randomness parameter
training_data, test_data = data_df.randomSplit([0.8, 0.2], seed=123)

training_data.show(5)

# Convert the CategoryIndex column to binary labels (0 or 1)
#  0 represents "ham" and 1 represents "spam"
training_data = training_data.withColumn("label", when(training_data["CategoryIndex"] == 0.0, 0).otherwise(1))

training_data.show(5)


# Define the MLP classifier model
layers = [len(data_df.select('features').first()[0]), 64, 2]
mlp_classifier = MultilayerPerceptronClassifier(layers=layers, labelCol="label", seed=42)

# Train the model
mlp_model = mlp_classifier.fit(training_data)

# Make predictions on the test data
predictions = mlp_model.transform(test_data)

predictions.select("Category","CategoryIndex", "prediction","Message","features").show(1000)

# Create a MulticlassClassificationEvaluator instance
evaluator = MulticlassClassificationEvaluator(labelCol="CategoryIndex", predictionCol="prediction", metricName="accuracy")

# Evaluate the model on the test data
accuracy = evaluator.evaluate(predictions)

# Print the accuracy
print("MultilayerPerceptronClassifier [Accuracy] = %g" % accuracy)
print("MultilayerPerceptronClassifier [Error] = %g" % (1.0 - accuracy))



# Save the MultilayerPerceptronClassifier model.
mlp_model.write().overwrite().save('mlp_model')

# Load the trained model
mlp_model= MultilayerPerceptronClassificationModel.load('mlp_model')