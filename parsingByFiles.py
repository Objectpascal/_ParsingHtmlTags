from parsingHtml import getFilePath;
from parsingHtml import getEncoding;
from parsingHtml import readHtmlFile;
from parsingHtml import HtmlFinder;
import threading;
import time ;

#findhtml = HtmlFinder("", endTag, encode, arrgs, False);  # class to find data
class TPrseByFiles(object):
    def __init__(self,pathCommands,pathHtml):
        '''

        :param pathCommands:this is the path of file that conant commands file
        :param pathHtml: this the path of file tha contant html file
        '''
        self.Lock=threading.Lock();
        self.Commands = self.readTheCommands(pathCommands);
        (self.encoding, self.dataHtml) = readHtmlFile(pathHtml);  # read the data content



    def start(self):
        self.startWoking(self.Commands,self.encoding,self.dataHtml);




    def startWoking(self,comands, encoding, data):
        '''

        :param comands:commands the u read by  readTheCommands(path) function
        :param encoding:the encoding of html file
        :param data: data in html file
        :return:None
        '''
        arrCommands = self.splitAllCommandsToArray(comands);
        if len(arrCommands) == 0:
            print("[-] the file commands its empty ..")
            exit();
        self.allJobs=len(arrCommands);
        self.finshedJobs=0;
        SaveFormat="Command_num_%d.txt";
        count=1;
        for spComm in arrCommands:
            value = spComm[0];
            endTag = spComm[1];
            fileSave=SaveFormat%(count);
            t=threading.Thread(target=self.Wroker,args=(value,endTag,encoding,data,fileSave))
            t.daemon=True;
            t.start();
            #self.Wroker(value,endTag,encoding,data,fileSave);
            count+=1;

        while(self.finshedJobs!=self.allJobs):
            time.sleep(2);

        print("finshed 100% done")


    def Wroker(self,value, endTag, encoding, data, filesave):
        '''

        :param value:value in commands file
        :param endTag:end tag in commands file
        :param encoding: encoding in html file
        :param data:data in html file
        :param filesave:path to save file
        :return: None
        '''
        # [(key,property value)];
        arrgs = [("", value)];
        findhtml = HtmlFinder("", endTag, encoding, arrgs, False, filesave);
        findhtml.feed(data);
        try:
            self.Lock.acquire();#lock th read whent change
            self.finshedJobs+=1;#inc the finhed jobs
        finally:
            self.Lock.release();#release to let ather thread chnge in value finshedJobs
    def splitValues(self,fullCommand):  # get values from commands text
        '''

        :param fullCommand: this the full comand value:endTag
        :return: return tupe of split command (value,endtag)
        '''
        if ":" not in fullCommand:
            fullCommand += ":";
        result = str(fullCommand).split(":");
        valueAttr = str(result[0]).strip();
        endTag = str(result[1]).strip();
        return (valueAttr, endTag);


    def readTheCommands(self,path):
        '''

        :param path: path of commands file
        :return: return array of data in commands file
        '''

        try:
            encoding=getEncoding(path);
            f = open(path, mode="r",encoding=encoding);#"sr.txt"
            Commands = f.readlines();
        finally:
            f.close();
            del f;

        return Commands;
    #split all coomnds to array
    def splitAllCommandsToArray(self,commands):
        '''

        :param commands:commands that u read by function readTheCommands(path)
        :return: return array of tupe of splited commands [(value,endtag),(value,endtag),...]
        '''
        result=[];
        for comm in commands:
            comm = str(comm).replace("\n", "");#remove the \n
            (valueAttr, endTag) = self.splitValues(comm);#split value to (val,endTag)
            if(str(endTag).strip()==""):
                pass;

            else:
                result.append((valueAttr, endTag));#add to the result array
        return result;#return the result

#----------main
def printShapeFast():
    shape='''
______        _     _____                     _
|  ___|      | |   /  ___|                   | |
| |_ __ _ ___| |_  \ `--.  ___  __ _ _ __ ___| |__   ___
|  _/ _` / __| __|  `--. \/ _ \/ _` | '__/ __| '_ \ / _ \
| || (_| \__ \ |_  /\__/ /  __/ (_| | | | (__| | | |  __/
\_| \__,_|___/\__| \____/ \___|\__,_|_|  \___|_| |_|\___|


    ''';
    print(shape);
def printshapebegin():
    shape='''
    (   (
     )   )
     ____
    |Tea |_
    |Cafe|_)
    \____/


    '''
    print(shape);
def main():
    printshapebegin();
    # read the command file
    print("-" * 30)
    pathCommands=getFilePath("[?] File Path < of Commands the contente combination of PropertyValue:endTag > ----> ");#"sr.txt"#
    print("\n" * 1);
    print("-" * 30)
    # read the html file
    pathHtml = getFilePath("[?] File Path < Html codes That you want to work on it  > ----> ");
    print("\n"*1);
    print("-"*30)

    print("[!] wait unit finshed ....")
    print();
    printShapeFast();
    prsingHtml=TPrseByFiles(pathCommands,pathHtml);
    prsingHtml.start();
    print("\n" * 3);
    print("-" * 30)
    input("[+]<All Done 100%>");


if __name__=="__main__":
    main();
