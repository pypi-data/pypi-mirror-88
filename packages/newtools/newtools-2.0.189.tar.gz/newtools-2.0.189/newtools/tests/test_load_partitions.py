import unittest
from newtools.aws import AthenaPartition, S3List
from newtools.db import AthenaClient


class TestLoadPartitions(unittest.TestCase):
    bucket = "newtools-tests-data"
    tablename = "load_partition_test_data"
    region = "eu-west-1"
    prefix = "load_partition_test_data/"
    database = "test_database"
    output_location = "s3://aws-athena-query-results-933373196108-eu-west-1/"
    source_file = "s3://newtools-tests-data/load_partition_test_data/"
    athena_client = None

    @classmethod
    def setUpClass(cls):
        cls.s3_list_folders = S3List(cls.bucket)
        cls.load_partitions = AthenaPartition(cls.bucket)
        cls.athena_client = AthenaClient(region=cls.region, db=cls.database, max_retries=2)

        cls.athena_client.add_query(
            f"""
            CREATE EXTERNAL TABLE IF NOT EXISTS {cls.tablename}(
                col1 string,
                col2 string,
                col3 string)
            PARTITIONED BY (year string, month string)
            ROW FORMAT SERDE
                'org.apache.hadoop.hive.serde2.OpenCSVSerde'
            STORED AS INPUTFORMAT
                'org.apache.hadoop.mapred.TextInputFormat'
            OUTPUTFORMAT
                'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
            LOCATION
                '{cls.source_file}'
            TBLPROPERTIES ('skip.header.line.count'='1')
            ;""", output_location=cls.output_location)

        cls.athena_client.add_query(
            f"""
            ALTER TABLE {cls.tablename} ADD IF NOT EXISTS 
                PARTITION (year='2019', month='02') LOCATION '{cls.source_file}year=2019/month=02/'
                PARTITION (year='2019', month='0:2') LOCATION '{cls.source_file}year=2019/month=0:2/'
                PARTITION (year='2020', month='01') LOCATION '{cls.source_file}year=2020/month=01/'

            ;""", output_location=cls.output_location)

        cls.athena_client.wait_for_completion()

    @classmethod
    def tearDownClass(cls):
        cls.athena_client.add_query(f"DROP TABLE {cls.tablename}", output_location=cls.output_location)
        cls.athena_client.wait_for_completion()

    def test_list_folder(self):
        folders = [{'Prefix': 'load_partition_test_data/year=2019/'}, {'Prefix': 'load_partition_test_data/year=2020/'}]
        test_folders = self.s3_list_folders.list_folders(self.prefix)
        self.assertListEqual(folders, test_folders)

    def test_list_partitions(self):
        partitions_list = [{'Prefix': 'load_partition_test_data/year=2019/month=02/some_more_directory/'},
                           {'Prefix': 'load_partition_test_data/year=2019/month=0:2/some_more_directory/'},
                           {'Prefix': 'load_partition_test_data/year=2020/month=01/some_more_directory/'},
                           {'Prefix': 'load_partition_test_data/year=2020/month=01/some_more_directory_1/'},
                           {'Prefix': 'load_partition_test_data/year=2020/month=02/some_more_directory/'}]
        test_partitions_list = self.load_partitions.list_partitions('load_partition_test_data')
        self.assertListEqual(partitions_list, test_partitions_list)

    def test_list_partitions_error(self):
        with self.assertRaises(ValueError):
            self.load_partitions.list_partitions()

    def test_get_sql(self):
        sql_query_list = [
            "ALTER TABLE load_partition_test_data ADD IF NOT EXISTS PARTITION(year='2019',month='02') LOCATION 's3://newtools-tests-data/load_partition_test_data/year=2019/month=02/some_more_directory/' PARTITION(year='2019',month='0:2') LOCATION 's3://newtools-tests-data/load_partition_test_data/year=2019/month=0:2/some_more_directory/' PARTITION(year='2020',month='01') LOCATION 's3://newtools-tests-data/load_partition_test_data/year=2020/month=01/some_more_directory/' PARTITION(year='2020',month='01') LOCATION 's3://newtools-tests-data/load_partition_test_data/year=2020/month=01/some_more_directory_1/' PARTITION(year='2020',month='02') LOCATION 's3://newtools-tests-data/load_partition_test_data/year=2020/month=02/some_more_directory/'"]
        test_sql_query_list = self.load_partitions.get_sql('load_partition_test_data')
        self.assertListEqual(sql_query_list, test_sql_query_list)

    def test_generate_sql(self):
        partitions_list = [{'Prefix': 'load_partition_test_data/year=2019/month=02/some_more_directory/'},
                           {'Prefix': 'load_partition_test_data/year=2019/month=0:2/some_more_directory/'},
                           {'Prefix': 'load_partition_test_data/year=2020/month=01/some_more_directory/'},

                           ]

        sql_query_list = [
            "ALTER TABLE load_partition_test_data ADD IF NOT EXISTS PARTITION(year='2019',month='02') LOCATION 's3://newtools-tests-data/load_partition_test_data/year=2019/month=02/some_more_directory/' PARTITION(year='2019',month='0:2') LOCATION 's3://newtools-tests-data/load_partition_test_data/year=2019/month=0:2/some_more_directory/' PARTITION(year='2020',month='01') LOCATION 's3://newtools-tests-data/load_partition_test_data/year=2020/month=01/some_more_directory/'"]

        sql_query_list_test = self.load_partitions.generate_sql('load_partition_test_data', partitions_list)
        self.assertListEqual(sql_query_list, sql_query_list_test)

    def test_generate_sql_with_client(self):
        partitions_list = [{'Prefix': 'load_partition_test_data/year=2019/month=02/'},
                           {'Prefix': 'load_partition_test_data/year=2019/month=0:2/'},
                           {'Prefix': 'load_partition_test_data/year=2020/month=01/'},
                           {'Prefix': 'load_partition_test_data/year=2020/month=02/'}]

        sql_query_list = [
            "ALTER TABLE load_partition_test_data ADD IF NOT EXISTS PARTITION(year='2020',month='02') LOCATION 's3://newtools-tests-data/load_partition_test_data/year=2020/month=02/'"]

        sql_query_list_test = self.load_partitions.generate_sql('load_partition_test_data', partitions_list,
                                                                athena_client=self.athena_client,
                                                                output_location=self.output_location)
        self.assertListEqual(sql_query_list, sql_query_list_test)

    def test_generate_sql_with_client_error(self):
        partitions_list = [{'Prefix': 'load_partition_test_data/year=2019/month=02/'},
                           {'Prefix': 'load_partition_test_data/year=2019/month=0:2/'},
                           {'Prefix': 'load_partition_test_data/year=2020/month=01/'}]

        with self.assertRaises(ValueError):
            self.load_partitions.generate_sql('load_partition_test_data', partitions_list,
                                              athena_client=self.athena_client)
