import os
def diskAnalyszer(filePath = None):
              if filePath == None:
                            return
              else:
                            disk(filePath)
              print("Done")

def fmt(num, suffix='B'):
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)

def disk(path):
              out = open("out.txt","w")
              lst = []
              lst.append(path)
              while (len(lst) != 0):
                            path = lst.pop(0)
                            for item in os.listdir(path):
                                          if item[0] != ".":
                                                        absolutePath = os.path.join(path,item)
                                                        if (os.path.islink(absolutePath)):
                                                                      continue
                                                        elif os.path.isdir(absolutePath):
                                                                      lst.append(absolutePath)
                                                                      out.write("Folder " + absolutePath +  " "+ fmt(os.path.getsize(absolutePath)))
                                                                      out.write("\n")
                                                        else:
                                                                      out.write("File " + absolutePath +  " "+ fmt(os.path.getsize(absolutePath)))
                                                                      out.write("\n")
              out.close()


def size(folderPath):
              if folderPath == None:
                            print "No Folder to Analyze"
                            return
              else:
                            print "Gathering File Size Data..."
                            tempFile = "tempFolderSize.txt"
                            outputFile = "SizeAnalysis.txt"
                            out = open(tempFile,"w")
                            folderSizeDataGatherer(folderPath,out)
                            out.close()
                            print "File Size Data Gathering Done"
                            infile = open(tempFile,"r")
                            content = infile.readlines()
                            infile.close()
                            #Remove temp file
                            sizeToFolderListMap = {}
                            sizeList = []
                            for line in content:
                                          lineC = line.split(" ,, ")
                                          path = lineC[0]
                                          size = eval(lineC[1])
                                          if size in sizeToFolderListMap:
                                                        sizeToFolderListMap[size].append(path)
                                          else:
                                                        tempList= []
                                                        tempList.append(path)
                                                        sizeToFolderListMap[size] = tempList
                                                        sizeList.append(size)
                            
                            sizeList.sort()
                            sizeList.reverse()
                            toShow = 0
                            print "Done Processing File "
                            if len(sizeList)  < 30:
                                          toShow = len(sizeList)
                            else:
                                          toShow = 30
                            outFile = open(outputFile,"w")
                            for i in range(0,toShow):
                                          outFile.write ("For Size " + fmt(sizeList[i]) + "\n")
                                          #print "For Size " + fmt(sizeList[i])
                                          for item in sizeToFolderListMap[sizeList[i]]:
                                                        outFile.write(item)
                                                        outFile.write("\n")
                                          outFile.write("\n")                                         
                            infile.close()
              print("Done")
              
def folderSizeDataGatherer(path,out):
              totalSize = 0
              for item in os.listdir(path):
                            if item[0] != ".":
                                          absolutePath = os.path.join(path,item)
                                          if (os.path.islink(absolutePath)):
                                                                      continue
                                          elif os.path.isdir(absolutePath):
                                                        folderSize = folderSizeDataGatherer(absolutePath,out)
                                                        totalSize += folderSize
                                                        #out.write(absolutePath + " ,, " + str(folderSize))
                                                        #out.write("\n")
                                          else:
                                                        fileSize = os.path.getsize(absolutePath)
                                                        totalSize += fileSize
              out.write(path + " ,, " + str(totalSize))
              out.write("\n")                           
              return totalSize
                                          
                            

              
