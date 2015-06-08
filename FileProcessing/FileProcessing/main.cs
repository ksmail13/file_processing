using System;
using System.Collections.Generic;
using System.IO;
using System.Text;
using FileProcessing.ExtendsHash;

namespace FileProcessing
{
    class ExtendHashMain
    {
        const bool DEBUG = false;
        Document<Record> d;

        public ExtendHashMain()
        {
            d = new Document<Record>();
        }

        /// <summary>
        /// 파일에서 데이터를 읽어 Record로 파싱한다.
        /// </summary>
        /// <param name="filePath"></param>
        /// <returns></returns>
        private IEnumerable<Record>
            GetRecordFromFile(string filePath)
        {
            System.IO.StreamReader file = new System.IO.StreamReader(filePath, Encoding.ASCII);
            string str;
            while((str = file.ReadLine()) != null)
            {
                Record r = new Record();
                string[] datas = str.Split(',');

                r.name = datas[0];
                r.phone = datas[1];
                r.address = datas[2];
                r.major = datas[3];

                yield return r;
            }

            file.Close();

        }

        /// <summary>
        /// 파일에서 데이터를 읽어와 Document에 추가한다.
        /// </summary>
        /// <param name="filePath">읽을 파일 경로</param>
        public void read(string filePath)
        {
            foreach (Record r in GetRecordFromFile(filePath))
            {
                if(DEBUG)
                    Util.log("try add item {0}", r);

                bool result = d.AddItem(r);

                if(DEBUG)
                    Util.log("add {0}",result?"success":"failed");

            }

            
            Util.log("Read finish document has {0} buckets and {1}levels", d.Count, d.GlobalDepth);
            
        }

        static void Main(string[] args)
        {
            StreamWriter writer = new StreamWriter("../../result.txt");
            Console.SetOut(writer);
            ExtendHashMain extendsHash = new ExtendHashMain();
            extendsHash.read("../../MOCK_DATA.csv");
            writer.Flush();
            writer.Close();
        }
    }
}
