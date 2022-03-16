resource "aws_s3_object" "codigo_spark" {
  bucket = aws_s3_bucket.datalake.id
  key    = "emr-code/pyspark/emr_job_spark.py"
  acl    = "private"
  source = "../etl/emr_job_spark.py"
  etag   = filemd5("../etl/emr_job_spark.py")

}
