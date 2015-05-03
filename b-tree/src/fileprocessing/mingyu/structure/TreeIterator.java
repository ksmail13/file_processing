package fileprocessing.mingyu.structure;

import java.util.Iterator;

/**
 * Created by 민규 on 2015-05-04.
 */
public interface TreeIterator<T extends Comparable> extends Iterator {
    void traverse(BTreeNode<T> curr);
}
