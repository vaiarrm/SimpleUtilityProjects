//package org.analysis.soucecode;
/* This class takes the root path and prints the duplicate files/directories in the path.
 * File/Directory comparison is based on: 1. File Name 2. File Size 3. Creation Date
 * startProcess() -> Starts the comparison job
 * reportGeneration() -> Generates the report: List the file/directory name and all the paths where it is located
 */


import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.NoSuchFileException;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.attribute.BasicFileAttributes;
import java.nio.file.attribute.FileTime;
import java.util.HashMap;
import java.util.LinkedList;


public class FileAnalysis {
    
    
    String path;
    int noOfFilesAnalyzed; // This for statistics purpose only.
    HashMap<FileAttribute, String> fileMap; // Stores the first instance of the file/directory and its path
    HashMap<FileAttribute, LinkedList<String>> similarFiles; // Stores subsequent instances of the file/directory and their paths
    
    private class FileAttribute{
        /*
         * This class stores the attributes of files that are used for comparison
         */
        private String fileName;
        private long fileSize;
        private FileTime fileCreationTime;
        private int hash;
        
        public FileAttribute(String fileName, long fileSize, FileTime fileCreationTime){
            this.fileName = fileName;
            this.fileSize = fileSize;
            this.fileCreationTime= fileCreationTime;
            this.hash = 0;
        }
        public boolean equals(Object y) {
            if (y == this) return true;
            if (y == null) return false;
            if (y.getClass() != this.getClass()) return false;
            final FileAttribute that = (FileAttribute) y;
            if(!((this.fileName.equals(that.fileName))&&(this.fileSize == that.fileSize)&&(this.fileCreationTime.equals(that.fileCreationTime))))
                return false;
            return true;
        }
        public int hashCode() {
            int h = this.hash;
            if (h == 0){
                /*
                 * 17 is a random choice. It could have been any number.
                 */
                h = 17;
                h = this.fileName.hashCode() + 31 * h;
                h = ((Long) this.fileSize).hashCode() + 31 * h;
                h = this.fileCreationTime.hashCode() +  31 * h;
            }
            this.hash = h;
            return h;
        }
    }
    
    //Constructor
    public FileAnalysis( String path) throws IOException{
        this.path = path;
        this.noOfFilesAnalyzed = 0;
        this.fileMap = new HashMap<FileAnalysis.FileAttribute, String>();
        this.similarFiles = new HashMap<FileAnalysis.FileAttribute, LinkedList<String>>();
    }
    
    // This method starts the process to compare files/Directories
    public void startProcess() throws IOException{
        System.out.println("Starting Process ...");
        
        /*
         Below is code is to implement recursive file traversal. Recursive file traversal
         creates a problem when folder structure is much deeper for stack to handle
         
         File[] files = new File(this.path).listFiles();
         RecursiveFilesTraversal(files);
         
         */
        LoopFileTraversal();
        System.out.println("Process Complete");
        
    }
    
    // To traverse the folder structure
    private void LoopFileTraversal() throws IOException{
        
        File fileStart = new File(this.path);
        // Checking if the given path is a symbolic link.
        // This application do not process symbolic link.
        Path path = Paths.get(fileStart.getAbsolutePath());
        if(Files.isSymbolicLink(path)) return;
        
        File[] filesArrayBeg = fileStart.listFiles();
        if (filesArrayBeg == null) return;
        
        LinkedList<File[]> fileQueue = new LinkedList<File[]>();
        fileQueue.addLast(filesArrayBeg);
        
        while(!(fileQueue.isEmpty())){
            try {
                File[] filesArrayLoop = fileQueue.removeFirst();
                if(filesArrayLoop == null) continue;
                for(File file:filesArrayLoop){
                    noOfFilesAnalyzed++;
                    if (file.isDirectory()) {
                        boolean toAdd = checkDuplicate(file);
                        if(toAdd){
                            File[] filesArrayAddToQueue = file.listFiles();
                            if(!(filesArrayAddToQueue == null)){
                                fileQueue.addLast(file.listFiles());
                            }
                        }
                    } else {
                        checkDuplicate(file);
                    }
                }
            } catch (NullPointerException e) {
                e.printStackTrace();
            }
        }
    }
    // Recursively goes through the directories - This method is not used.
    // This is here for academic purpose.
    private void RecursiveFilesTraversal(File[] files) throws IOException {
        if(files == null){
            return;
        }
        for (File file : files) {
            if (file.isDirectory()) {
                checkDuplicate(file);
                RecursiveFilesTraversal(file.listFiles());
            } else {
                checkDuplicate(file);
            }
        }
    }
    /*
     * Generates Report in the below format
     * File/Directory Name - <Name>
     * 			<File Path 1>
     * 			<File Path 2>
     * 			<File Path n>
     * File/Directory Name - <Name>
     * 			<File Path 1>
     * 			<File Path 2>
     */
    public void generateReport(){
        for(FileAttribute key : similarFiles.keySet()){
            System.out.println("File/Directory Name - " + key.fileName);
            String firstPathName = fileMap.get(key);
            System.out.printf("\t\t %s\n",firstPathName);
            LinkedList<String> list = similarFiles.get(key);
            for(String pathName:list){
                System.out.printf("\t\t %s\n",pathName);
            }
            System.out.println(" ");
        }
    }
    
    /*
     * if key is present in fileMap then that file is duplicate. The duplicate record is put in the similarFiles HashMap
     * if key is not present in fileMap HashMap then it is the first instance. This new instance is recorded in fileMap HashMap.
     * This method will not process if the path is a symbolic link or application donot have
     * permission to access that path
     */
    
    private boolean checkDuplicate(File file) throws IOException{
        try {
            Path path = Paths.get(file.getAbsolutePath());
            if(Files.isSymbolicLink(path)) return false; // Check for symbolic link
            if(!(Files.isReadable(path))) return false;  // Check for Access
            BasicFileAttributes attr = Files.readAttributes(path, BasicFileAttributes.class);
            
            FileAttribute fileAttribute = new FileAttribute(file.getName(), attr.size(), attr.creationTime());
            
            if(fileMap.containsKey(fileAttribute)){
                if(!(similarFiles.containsKey(fileAttribute))){
                    similarFiles.put(fileAttribute, new LinkedList<String>());
                }
                LinkedList<String> similarFileLL = similarFiles.get(fileAttribute);
                similarFileLL.add(file.getAbsolutePath());
                return false;
            }else{
                fileMap.put(fileAttribute, file.getAbsolutePath());
                return true;
            }
            
        } catch (NoSuchFileException e) {
            //e.printStackTrace();
            System.out.println("Error NoSuchFileException:" + file.getAbsolutePath());
        }catch (IOException e) {
            //System.out.println("Error IOException:" + file.getAbsolutePath());
            e.printStackTrace();
        }catch (Exception e){
            System.out.println("Error Exception:" + file.getAbsolutePath());
            e.printStackTrace();
        }
        return true;
    }
    
    public static void main (String[] args) throws IOException {
        long start	= 0;
        long now 	= 0;
        
        try {
            //FileAnalysis fa = new FileAnalysis("/Volumes/MS-DOS");
            FileAnalysis fa = new FileAnalysis("/");
            start = System.currentTimeMillis();
            fa.startProcess();
            now = System.currentTimeMillis();
            fa.generateReport();
            System.out.println("Final Stats - " + fa.noOfFilesAnalyzed);
            System.out.println((now-start)/1000);
        } catch (IOException e) {
            e.printStackTrace();
        }
        
    }
}
