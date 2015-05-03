package fileprocessing.mingyu.structure;

import fileprocessing.mingyu.util.SortedArrayList;

import java.util.ArrayList;
import java.util.Iterator;

/**
 * Created by 민규 on 2015-05-04.
 * Comparable 클래스를 상속한 클래스를 키로 삼아 트리를 생성한다.
 */
public class BTree<T extends Comparable> implements Iterable {
    private BTreeNode<T> mRoot;
    private int mDegree;

    /**
     * 트리 생성
     * @param degree 차수
     */
    public BTree(int degree) {
        mRoot = new BTreeNode<T>(null, degree);
        this.mDegree = degree;
    }

    /**
     * 트리에 노드를 추가한다.
     * @param object 추가할 객체
     * @return
     */
    public boolean add(T object) {
        BTreeNode<T> curr = mRoot;
        boolean result = false;
        // find insert node
        find:while(true) {
            SortedArrayList<T> value_list = curr.getValues();
            int insert_pos = value_list.findInsertPosition(object);

            if(curr.getChild(insert_pos) != null) {
                curr = curr.getChild(insert_pos);
                continue;
            }
            else {
                if(!curr.isFull()) {
                    value_list.addObject(object);
                }
                else {
                    split(curr, object);
                }

                result = true;
                break;
            }
        }

        return result;
    }

    /**
     * 노드를 분리한다.
     * @param node 데이터를 넣으려는 노드
     * @param object 넣으려는 데이터
     */
    private void split(BTreeNode<T> node, T object) {
        int i;
        // insert data in node
        node.addValue(object);
        // get mid value
        T mid_value = (T) node.getValues().get(node.valueSize()/2);
        BTreeNode<T> parent = node.getParent();
        BTreeNode<T> sibling_node = null;
        boolean isNewRoot = false;

        // if node is root then make new root
        if(parent == null) {
            parent = new BTreeNode<T>(null, mDegree);
            mRoot = parent;
            node.setParent(parent);
            isNewRoot = true;
        }

        // when node is not root
        if (!parent.isFull()) {
            parent.addValue(mid_value);
        } else {
            // if parent full then call split method for split parent node
            split(parent, mid_value);
            parent = node.getParent();
        }


        // move value that bigger then mid_value to next sibling node
        int mid_index = parent.indexOfFromValues(mid_value);

        if(isNewRoot) {
            parent.setChild(node, mid_index);
            parent = node.getParent();
        }

        sibling_node = parent.getChild(mid_index+1);
        if(sibling_node == null) {
            sibling_node = new BTreeNode<T>(parent, mDegree);
            parent.setChild(sibling_node, mid_index + 1);
        }
        int nodeValueCount = node.valueSize();
        for (i = nodeValueCount-1 ; i > nodeValueCount/2; i--) {
            if(sibling_node.isFull() == false) {
                BTreeNode<T> temp;
                int index = sibling_node.addValue((T) node.getValues().get(i));
                node.removeValue(i);
                temp = node.getChild(i+1);
                if(temp != null) temp.setParent(sibling_node);
                sibling_node.addChild(temp, index+1);
                node.removeChild(i+1);
            }
            else
                split(sibling_node, (T)node.getValues().get(i));
        }

        // remove mid_value from node
        node.getValues().remove(mid_value);
        sibling_node.setChild(node.getChild(i + 1), 0);
        node.removeChild(i+1);
    }

    public boolean remove(T object) {
        return false;
    }

    public boolean search(T object) {
        return false;
    }

    // implement Iterable interface

    /**
     * traverse in b tree
     * @param <T>
     */
    class BTreeInorderIterator<T extends Comparable> implements TreeIterator<T> {
        private int mPos;
        private ArrayList<T> mDataList;


        BTreeInorderIterator(BTreeNode<T> root) {
            mDataList = new ArrayList<T>();
            mPos = 0;

            traverse(root);
        }

        /**
         * traverse tree by inorder algorithm
         * @param curr
         */
        @Override
        public void traverse(BTreeNode<T> curr) {
            int i;
            for(i=0;i<curr.valueSize();i++) {
                if(curr.getChild(i) != null) {
                    traverse(curr.getChilds().get(i));
                }
                mDataList.add((T)curr.getValues().get(i));
            }

            if(curr.getChild(i) != null) {
                traverse(curr.getChilds().get(i));
            }

        }

        @Override
        public boolean hasNext() {
            return mPos != mDataList.size();
        }

        @Override
        public T next() {
            return mDataList.get(mPos++);
        }
    }

    /**
     * traverse in b tree
     * @param <T>
     */
    class BTreePostorderIterator<T extends Comparable> implements TreeIterator<T>{
        private int mPos;
        private ArrayList<T> mDataList;


        BTreePostorderIterator(BTreeNode<T> root) {
            mDataList = new ArrayList<T>();
            mPos = 0;

            traverse(root);
        }

        @Override
        public boolean hasNext() {
            return mPos != mDataList.size();
        }

        @Override
        public T next() {
            return mDataList.get(mPos++);
        }

        /**
         * traverse tree by inorder algorithm
         * @param curr
         */
        @Override
        public void traverse(BTreeNode<T> curr) {
            int i;
            for(i=0;i<=curr.valueSize();i++) {
                if(curr.getChild(i) != null) {
                    traverse(curr.getChilds().get(i));
                }
            }

            for (int j = 0; j < curr.valueSize(); j++) {
                mDataList.add((T)curr.getValues().get(j));
            }
        }
    }


    @Override
    public Iterator iterator() {
        return new BTreePostorderIterator(mRoot);
    }
}
