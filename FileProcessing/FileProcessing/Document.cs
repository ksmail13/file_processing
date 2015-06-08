using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace FileProcessing
{
    namespace ExtendsHash { 
        
        class Document<T>
        {
            const bool DOCUMENT_DEBUG = true;

            private Bucket<T>[] mDocument;
            private int mDepth;
            private int mCount;

            public int Count { get { return mCount; } }

            public int GlobalDepth
            {
                get { return mDepth; }
            }

            public Document()
            {
                mCount = 2;
                mDocument = new Bucket<T>[mCount];
                mDocument[0] = new Bucket<T>(this);
                mDocument[0].Hash = 0;
                mDocument[1] = new Bucket<T>(this);
                mDocument[1].Hash = 1;
                mDepth = 1;
            }

            /// <summary>
            /// 데이터를 추가한다.
            /// </summary>
            /// <param name="item">추가할 데이터</param>
            /// <returns>추가 여부</returns>
            public bool AddItem(T item)
            {
                int hash = Util.PaddedHash(GlobalDepth, item);
                Bucket<T> selectedBucket = mDocument[hash];
                switch (selectedBucket.AddRecord(item))
                {
                    case BucketOperationResult.FAILED:
                        return false;
                    case BucketOperationResult.SPLIT:
                        if(selectedBucket.BucketLevel == GlobalDepth)
                        {
                            // 버킷의 깊이가 도큐먼트의 깊이와 같다면 확장한다.
                            ExtendDocument(hash);
                        }
                        else
                        {
                            // 버킷의 깊이가 도큐먼트의 깊이보다 낮으면 단순 분리한다.
                            SplitBucket(hash, selectedBucket);
                        }
                        return AddItem(item);
                    case BucketOperationResult.SUCCESS:
                        //Util.log("add item finish");
                        return true;
                }


                return false;
            }

            /// <summary>
            /// 버켓을 나눈다.
            /// </summary>
            /// <param name="hash"></param>
            /// <param name="selectedBucket"></param>
            private void SplitBucket(int hash, Bucket<T> selectedBucket)
            {
                if (DOCUMENT_DEBUG)
                {
                    Util.log("Split Bucket! from hash {0}", hash);
                }
                // 버캣의 깊이 증가
                selectedBucket.BucketLevel++;
                int bucketPadding = Util.GeneratePadding(selectedBucket.BucketLevel);
                int createIndex = hash & bucketPadding;
                // 데이터가 들어갈 버켓 생성
                mDocument[createIndex] = new Bucket<T>(this);
                Bucket<T> newBucket = mDocument[createIndex];
                // 해시정보 초기화
                newBucket.BucketLevel = selectedBucket.BucketLevel;
                newBucket.Hash = Util.BitOn(selectedBucket.BucketLevel, selectedBucket.Hash);
                // 데이터 분리
                for(int i=0;i<selectedBucket.Lists.Count;i++)
                {
                    T record = selectedBucket.Lists[i];
                    if (!selectedBucket.IsCorrectHash(record))
                    {
                        newBucket.Lists.Add(record);
                        selectedBucket.Lists.Remove(record);
                        i--;
                    }
                }

                mCount++;
            }


            /// <summary>
            /// split이 발생한 버킷의 인덱스
            /// </summary>
            /// <param name="extendIndex"></param>
            private void ExtendDocument(int extendIndex)
            {
                mDepth++;
                if(DOCUMENT_DEBUG)
                {
                    Util.log("Extend document! from index {0}", extendIndex);
                }
                Bucket<T>[] temp = new Bucket<T>[mDocument.Length * 2];
                for(int i=0;i<mDocument.Length;i++)
                {
                    if(extendIndex != i)
                    {
                        temp[i] = mDocument[i];
                        temp[mDocument.Length + i] = mDocument[i];
                    }
                    else
                    {
                        // 원인이 되는 부분에 버킷을 새로 생성하고
                        // 데이터를 분배한다.
                        temp[i] = mDocument[i];
                        mDocument[i].BucketLevel++;
                        temp[i + mDocument.Length] = new Bucket<T>(this);
                        temp[i + mDocument.Length].Hash = Util.BitOn(mDocument[i].BucketLevel, temp[i].Hash);
                        temp[i + mDocument.Length].BucketLevel = mDocument[i].BucketLevel;
                        Bucket<T> selectedBucket = temp[i], newBucket = temp[i + mDocument.Length];
                        // 데이터 분리
                        for (int j = 0; j < selectedBucket.Lists.Count; j++)
                        {
                            T record = selectedBucket.Lists[j];
                            if (!selectedBucket.IsCorrectHash(record))
                            {
                                newBucket.Lists.Add(record);
                                selectedBucket.Lists.Remove(record);
                                j--;
                            }
                        }
                        mCount++;
                    }
                }

                mDocument = temp;
            }

        }
    }
}
