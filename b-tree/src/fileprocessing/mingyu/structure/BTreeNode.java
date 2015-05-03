package fileprocessing.mingyu.structure;

import fileprocessing.mingyu.util.SortedArrayList;

import java.util.ArrayList;

/**
 * Created by 민규 on 2015-05-04.
 */
public class BTreeNode<T extends Comparable> {
    private BTreeNode mParent;

    private SortedArrayList<T> mValues;
    private ArrayList<BTreeNode<T>> mChilds;

    private int mDegree;

    public BTreeNode(BTreeNode<T> parent, int degree)
    {
        mParent = parent;
        mDegree = degree;
    }

    public void setParent(BTreeNode<T> parent) {
        mParent = parent;
    }

    public BTreeNode<T> getParent()
    {
        return mParent;
    }

    public T getValue(int i) {
        if(getValues().size() == 0)
            return null;
        return (T) getValues().get(i);
    }

    public boolean removeValue(int i) {
        if(i >= getValues().size()) {
            return false;
        }
        getValues().remove(i);
        getValues().add(null);
        return true;
    }

    public SortedArrayList<T> getValues() {
        if(mValues == null) {
            mValues = new SortedArrayList<T>(mDegree);
            for (int i = 0; i < mDegree; i++) {
                mValues.add(null);
            }
        }
        return mValues;
    }

    public BTreeNode<T> getChild(int i) {
        if(getChilds().size() == 0 || getChilds().size() <= i)
            return null;
        return mChilds.get(i);
    }

    public boolean removeChild(int i) {
        if(i >= getChilds().size()) {
            return false;
        }
        getChilds().remove(i);
        getChilds().add(null);
        return true;
    }

    public ArrayList<BTreeNode<T>> getChilds() {
        if(mChilds == null) {
            mChilds = new ArrayList<BTreeNode<T>>(mDegree+1);
            for (int i = 0; i < mDegree+1; i++) {
                mChilds.add(null);
            }
        }
        return mChilds;
    }

    public int addValue(T object) {
        int result = -1;
        if(isRealFull() == false) {
            result = mValues.addObject(object);
            if(result != -1) {
                // child follow value
                getChilds().add(result+1, null);
            }
        }

        return result;
    }

    private boolean isRealFull() {
        return getValues().size() == this.mDegree;
    }

    public void setChild(BTreeNode<T> child, int i) {
        if(getChilds().size() <= i) {
            getChilds().add(i, child);
        }
        else {
            getChilds().set(i, child);
        }
    }

    public void addChild(BTreeNode<T> child, int i) {
        getChilds().add(i, child);
    }

    public boolean isFull() {
        return getValues().size() >= this.mDegree-1;
    }

    public boolean isEnough() {
        return getValues().size() > this.mDegree/2;
    }

    public int valueSize() {
        return getValues().size();
    }

    public int childSize() {
        return getChilds().size();
    }

    public int indexOfFromValues(T object) {
        return getValues().indexOf(object);
    }

}
