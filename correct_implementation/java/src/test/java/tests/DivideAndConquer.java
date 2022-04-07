/**
 * Declare: the question and the find_single method are designed and
 *          written by professor Ting Hu from Queen's University.
 */

package tests;

public class DivideAndConquer {

//    public static void main(String[] args){
//    // only for testing the functionality of these algorithmns
//        String s = "e";
//        System.out.println(error_find_single(s,0,s.length()-1));
//
//    }

    public static Integer find_single(String s, Integer start, Integer end){

        if (start > end){
            return null;
        }
        else if (start == end){
            return start;
        }
        else{

            Integer mid = (end+start)/2;

            if (mid%2==0){
                if (s.charAt(mid)==s.charAt(mid+1)){
                    return find_single(s,mid+2,end);
                } else{
                    return find_single(s, start, mid);
                }
            }else{
                if (s.charAt(mid)==s.charAt(mid-1)){
                    return find_single(s,mid+1,end);
                } else{
                    return find_single(s,start,mid-1);
                }
            }
        }
    }

    public static Integer error_find_single(String searchString, Integer start, Integer end){

        if (searchString.length()%2==0) {
            return null;

        } else if (searchString.length()==1){ // missing this else-if statement so this solution was incorrect
            return 0;

        } else if (searchString.length()==3){

            int midString = searchString.charAt(1);
            int first = searchString.charAt(0);

            if (midString==first){
                return 2;
            } else{
                return 0;
            }
        } else {

            int mid = searchString.length() / 2;
            int midString = searchString.charAt(mid);
            int midStringMinus = searchString.charAt(mid-1);
            String firstHalf;
            String secondHalf;

            if (midString==midStringMinus){
                firstHalf = searchString.substring(0, mid+1);
                secondHalf = searchString.substring(mid+1);

            } else {
                firstHalf = searchString.substring(0, mid);
                secondHalf = searchString.substring(mid);

            }

            if (firstHalf.length()%2 == 0){
                return error_find_single(secondHalf, 0, secondHalf.length()+1) + firstHalf.length();
            } else {
                return error_find_single(firstHalf, 0, firstHalf.length()+1);
            }
        }
    }
}
