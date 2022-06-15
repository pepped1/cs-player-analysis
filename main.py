import os

from awpy.parser import DemoParser
from awpy.analytics.stats import player_stats

class demoTools:
    def __init__(self):
        self.demFolder = "./cs_demos/"
        self.parFolder = "./cs_demos_parsed/"
        self.parseRate = 128
        self.player = 0
        # Steam ID of player being processed

    def checkForParsed(self):
    # Checks if demos have existing parsed data
        existingDemos = set()
        for filename in os.listdir(self.parFolder):
            if filename.endswith(".json"):
                existingDemos.add(filename[:-5])

        return existingDemos

    def parseDemos(self, returnFormat="json"):
    # Parses all demos in the "demFolder" folder as either JSON or DF format.
    # Parsed demos are saved as JSON files in "parFolder" folder.
    # Returns a list of dataframes
        
        existingDemos = self.checkForParsed()
        #print(existingDemos)
        demos = []
        for filename in os.listdir(self.demFolder):
            if filename.endswith(".dem"):
                title = filename[:-4]
                file = os.path.join(self.demFolder, filename)
                if title not in existingDemos:
                    print("creating json")
                    demoParser = DemoParser(
                        demofile = file,
                        demo_id = title,
                        outpath = self.parFolder,
                        parse_rate = self.parseRate,
                        buy_style = "hltv"
                    )
                    
                    demo = demoParser.parse(return_type=returnFormat)
                    demos.append(demo)
                else:
                    print("found demo")
                    demoParser = DemoParser(
                        demofile = file,
                        demo_id = title,
                        parse_rate = self.parseRate,
                        buy_style = "hltv"
                    )
                    json_path = os.path.join(self.parFolder, title + ".json") 
                    print(json_path)
                    demo = demoParser.read_json(json_path)
                    demos.append(demo)
            
        return demos
    
    def displayData(self):
        pass

p1 = demoTools()
data = p1.parseDemos()

player_stats_json = player_stats(data[0]["gameRounds"])
print(player_stats_json[p1.player])