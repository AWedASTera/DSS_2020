import os
import grpc
import time
import razdel
import logging
import pyspark
import summarizer_pb2
import summarizer_pb2_grpc
from concurrent import futures
from lexrank_model import LexRank

# set log level & disable pyspark logs:
logging.basicConfig(level=logging.DEBUG)
s_logger = logging.getLogger('py4j.java_gateway').setLevel(logging.ERROR)

# init LexRank:
logging.info("Initializing LexRank with precounted idf")
lxr = LexRank(path_to_idf_pickle='weights/idf.pickle')

# init Spark context:
logging.info("Initializing PySpark context")
sc = pyspark.SparkContext(os.getenv('SPARK_ADDRESS', 'local[*]'))


# define data transfromation to proto entity method:
def summarize_text_with_lex_rank(doc):
    summary = lxr.get_prediction_lex_rank(doc.text)
    processedIn = int(round(time.time() * 1000))
    return summarizer_pb2.TextToSummary(id=doc.id, text=doc.text, summary=summary, processedIn=str(processedIn))


# gRPC server implementation:
class SummarizerServicer(summarizer_pb2_grpc.SummarizerServicer):

    # override service method:
    def summarize(self, request, context):
        # get data from request:
        docs = request.textToSummary

        logging.info('Processing of %s text(s)', len(docs))

        # modify data - set summary and processing time:
        updated_docs = sc.parallelize(docs) \
            .map(lambda doc: summarize_text_with_lex_rank(doc)) \
            .collect()

        # return SummarizeResponse:
        return summarizer_pb2.SummarizeResponse(textToSummary=updated_docs)


# server startup:
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    summarizer_pb2_grpc.add_SummarizerServicer_to_server(
        SummarizerServicer(), server)
    logging.info('Started server on localost:6066')
    server.add_insecure_port('[::]:6066')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
