using System;
using System.Collections.Generic;

namespace FileProcessing
{

    namespace ExtendsHash
    {
        /// <summary>
        /// 데이터를 담을 버킷
        /// </summary>
        class Bucket<T>
        {
            const bool BUCKET_DEBUG = true;

            /// <summary>
            /// 버킷 기본 최대 사이즈
            /// </summary>
            public const uint BASIC_SIZE = 3;

            /// <summary>
            /// 버킷의 해시값
            /// </summary>
            public int Hash{ get; set; }

            /// <summary>
            /// 버킷 내부의 레코드
            /// </summary>
            private List<T> mRecords;

            /// <summary>
            /// 현재 레코드 갯수
            /// </summary>
            private int mCount;

            /// <summary>
            /// 버킷 최대 사이즈
            /// </summary>
            private uint mMaxRecordSize;

            /// <summary>
            /// 현재 버킷의 지역깊이
            /// </summary>
            private int mCheckLevel;

            /// <summary>
            /// 지역깊이 컨트롤을 위한 외부 인터페이스
            /// </summary>
            public int BucketLevel
            {
                get
                {
                    return mCheckLevel;
                }

                set
                {
                    if (value > Parent.GlobalDepth) return;
                    mCheckLevel = value;
                }
            }

            public List<T> Lists
            {
                get { return mRecords; }
            }
            
            /// <summary>
            /// 버켓이 모두 차있는지 확인
            /// </summary>
            public bool IsFull
            {
                get { return mMaxRecordSize == mRecords.Count; }
            }

            /// <summary>
            /// 추가 버킷을 사용하기 위한 링크
            /// </summary>
            private Bucket<T> ExtraBucket = null;

            private Document<T> Parent = null;

            public Bucket(Document<T> parent, uint size = BASIC_SIZE)
            {
                Parent = parent;
                mMaxRecordSize = size;
                mRecords = new List<T>((int)size);
                mCount = 0;
                mCheckLevel = 1;
            }

            public bool IsCorrectHash(T item)
            {
                return Hash == Util.PaddedHash(BucketLevel, item);
            } 

            public BucketOperationResult AddRecord(T r)
            {
                if (!IsFull)
                {
                    if (BUCKET_DEBUG)
                    {
                        Util.log("bucket add to bucket");
                    }
                    mRecords.Add(r);
                    return BucketOperationResult.SUCCESS;
                }
                else
                {
                    BucketOperationResult result = BucketOperationResult.FAILED;
                    int hash = Util.PaddedHash(BucketLevel+1, r);
                    // 다른 해시가 섞여 있는지 확인한다.
                    foreach(T record in mRecords)
                    {
                        int recordHash = Util.PaddedHash(BucketLevel+1, record);
                        if (hash != recordHash)
                        {
                            result = BucketOperationResult.SPLIT;
                            break;
                        }
                    }

                    if (result == BucketOperationResult.FAILED)
                    {
                        return AddRecordToExtraBucket(r);
                    }
                    return result;
                }
            }

            private BucketOperationResult AddRecordToExtraBucket(T r)
            {
                if (ExtraBucket == null) ExtraBucket = new Bucket<T>(Parent);
                if (BUCKET_DEBUG)
                {
                    Util.log("bucket add record to extra bucket");
                }
                return ExtraBucket.AddRecord(r);
            }
            public BucketOperationResult RemoveRecord(T r)
            {
                mRecords.Remove(r);
                return BucketOperationResult.FAILED;
            }
        }
    }
}
