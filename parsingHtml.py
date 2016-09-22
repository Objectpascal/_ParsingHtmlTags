from html.parser import HTMLParser;


class HtmlFinder(HTMLParser):
    def __init__(self, startTag, endTag, encode, attrs=[], byTag=True,SavePath="result.txt"):
        super(HtmlFinder, self).__init__();
        self.startTag = startTag;
        self.endTag = endTag;
        self.attrs = attrs;
        self.isInRange = False;
        self.file = open(SavePath, "w", encoding=encode, errors='replace');  # ,errors='replace';
        self.byTag = byTag;

    def handle_starttag(self, tag, attrs):
        if not self.byTag:
            if not self.isInRange:
                self.isInRange = self.testMatcheAny(attrs);

        else:
            if not self.isInRange:  # if not start it :p
                # do some test to figer out were is the strat tag


                # finx the tag exple <p> --> p
                FixStartTag = self.startTag;
                FixStartTag = str(FixStartTag).replace("<", "");
                FixStartTag = str(FixStartTag).replace(">", "");
                if tag == FixStartTag:
                    self.isInRange = self.testMatcheAny(attrs);

    def testMatcheAny(self, tagAttrs):
        matchCount = len(self.attrs);
        if matchCount == 0:
            return True;

        for atr in self.attrs:
            for tgAtr in tagAttrs:
                if (str(tgAtr[0]).lower() == str(atr[0]).lower()) or (str(atr[0]).strip() == ""):
                    if str(atr[1]).lower() in str(tgAtr[1]).lower():
                        matchCount -= 1;
        if matchCount <= 0:
            return True
        else:
            return False;

    def handle_endtag(self, tag):

        # finx the tag exple </p> --> p
        if self.isInRange:
            FixStartTag = self.endTag;
            FixStartTag = str(FixStartTag).replace("<", "");
            FixStartTag = str(FixStartTag).replace(">", "");
            FixStartTag = str(FixStartTag).replace("/", "");
            if tag == FixStartTag:
                self.isInRange = False;

    def handle_data(self, data):
        if self.isInRange:
            # print("[+] Data ->",str(data).strip());
            if str(data).strip()!="":
                 self.file.write(str(data).strip() + "\n");

    def __del__(self):
        if not self.file.closed:
            self.file.close();
            del self.file;

def readHtmlFile(filePath):
    try:
        encode = getEncoding(filePath);
        f = open(filePath, "r", encoding=encode);  # errors='replace'  # open file
        data = f.read();  # read the html code

        return (encode,data);
    finally:
        f.close();  # close the file
        del f;  # delete object f
def main():
    filePath = getFilePath("[?] File Path < That you want to work on it > ----> ");  # get valid file path
    (encode,data)=readHtmlFile(filePath);
    startTag = "";
    print("-" * 30);

    byTag = itsByTag();
    if byTag:
        print("[+] now you work with Tag and Proerty\n");
        startTag = input("[?] Start Tag <Tag(example:<html>) ->");  # start tag
        print("-" * 30);
        arrgs = haveArgs(byTag);  # args

    else:
        print("-" * 30);
        print("[+] now you work Only With Proerty\n");
        arrgs = getArrgs();

    print("\n");
    print("-" * 30);
    endTag = input("[?] End Tag ->");  # end tag
    print("-" * 30);
    print("\n" * 5);
    findhtml = HtmlFinder(startTag, endTag, encode, arrgs, byTag);  # class to find data
    findhtml.feed(data);  # start find data
    print("\n" * 5);

    print("[+]<Done !>");
    input("<Entre to Exit>");


def itsByTag():
    ans = "";
    while str(ans).upper() not in ["Y", "N"]:
        ans = input("[?]do you want to work Only By Tag with proeprty? y/n->");
    if str(ans).upper() == "Y":  # if has args call getArrgs method
        return True;
    else:
        return False;


def getFilePath(mess):  # get valid file path
    import os;
    filePath = "";
    while not os.path.isfile(filePath):
        filePath = input(mess);
        if not os.path.isfile(filePath):
            print("[-] <invalid file name :%s>" % str(filePath));
            print("\n");
    return filePath;


def haveArgs(byTag):  # is have args?y/n
    ans = "";
    result = [];
    while str(ans).upper() not in ["Y", "N"]:
        ans = input("[?] do you have proeprty To put it in the search ?y/n->");
    if str(ans).upper() == "Y":  # if has args call getArrgs method
        result = getArrgs();
    return result;


def getArrgs():  # get arrgs array of tuple
    key = "";
    result = [];
    print("[!] Plz Put the property(key=Value) Example(id=10) <if key='' then the key its ignore>: \n\n");
    print("[!] < key = 5 to exit >")
    count = 1;
    while str(key).strip() != "5":
        print("[!] < key = 5 to exit >\n\n")
        print();
        key = input("[?] key[%d] ->" % count);  # input the key exmp : class
        if str(key).strip() != "5":
            value = input("[?] value[%d] ->" % count);  # input value exp : divclass
            newVal = (str(key), str(value));  # new type
            result.append(newVal);  # add to resullt array this well be return
            count += 1;
    return result;


def getEncoding(filePath):
    types_of_encoding = ["utf-8", "cp1252", "utf-16", "utf-32"]
    for encoding_type in types_of_encoding:
        try:
            f = open(filePath, "r", encoding=encoding_type);  # open file
            data = f.read();
            f.close();
            return encoding_type;
        except:
            pass;
    return "";


if __name__ == "__main__":
    main();  # main method
