package fileprocessing.mingyu;

import fileprocessing.mingyu.structure.BTree;

import java.util.Iterator;

public class Main {
    public final static int DEGREE = 5;
    public final static int []DATA_SET = {69, 7, 150, 19, 70, 20, 128, 18, 42, 120, 140, 16, 100, 26,
            145, 15, 110, 30, 40, 132, 138, 50, 43, 130, 136, 41, 59, 54, 122, 124};

    public static void main(String[] args) {
        BTree<Integer> tree = new BTree<Integer>(5);

        for (int i = 0; i < DATA_SET.length; i++) {
            System.out.printf("%-5d : ", DATA_SET[i]);
            tree.add(DATA_SET[i]);

            Iterator it = tree.iterator();

            while(it.hasNext()) {
                System.out.printf("%d ",it.next());
            }
            System.out.println();
        }


    }
}
