package fileprocessing.mingyu.util;

import java.util.ArrayList;

/**
 * 데이터 입력시 정렬되어 저장되는 클래스
 * @param <T> 저장할 데이터 클래스 Comparable interface를 구현해야한다.
 */
public class SortedArrayList<T extends Comparable> extends ArrayList
{
    public SortedArrayList(int i) {
        super(i);
    }

    @Override
    public boolean add(Object o) {
        return addObject(o) != -1;
    }

    public int addObject(Object o) {
        int result = -1;
        if(o != null) {
            T newObj = (T)o;
                /*for (int i = 0; i < this.size(); i++) {
                    if(newObj.compareTo(get(i)) < 0) {
                        addObject(i, o);
                        result = true;
                        break;
                    }
                }*/
            result = findInsertPosition(newObj);
            add(findInsertPosition(newObj), newObj);
        }
        return result;
    }

    /**
     * 이진탐색을 통해 o를 찾는다.
     * @param o
     * @return 찾으면 인덱스 못찾으면 -1
     */
    @Override
    public int indexOf(Object o) {
        int left = 0;
        int right = size();
        if(o == null) return -1;
        T find_obj = (T)o;

        while(right-left >= 1) {
            int mid = (left+right)/2;
            int cmpResult = find_obj.compareTo(get(mid));
            if(cmpResult < 0) {
                right = mid;
            }
            else if(cmpResult > 0){
                left = mid+1;
            }
            else {
                return mid;
            }
        }

        return -1;
    }

    /**
     *  이진 탐색을 이용해 입력될 위치를 찾는다.
     * @param o
     * @return
     */
    public int findInsertPosition(T o) {
        int left = 0;
        int right = size();

        while(right-left >= 1) {
            int mid = (left+right)/2;
            int cmpResult = o.compareTo(get(mid));
            if(cmpResult < 0) {
                right = mid;
            }
            else if(cmpResult > 0){
                left = mid+1;
            }
            else {
                right = mid;
                break;
            }
        }

        return right;
    }

}
