class ColourGenerator:
    def getPremierLeagueColoursRGBA(self, data):
        results = []
        for i in data:
            dict = {}
            if i == 'Arsenal':
                dict['team'] = i
                dict['colour'] = 'rgba(242,38,19,0.8)' #Red
                
            elif i == 'Aston Villa':
                dict['team'] = i
                dict['colour'] = 'rgba(150,54,148,0.8)' #Violet
                
            elif i == 'Brighton':
                dict['team'] = i
                dict['colour'] = 'rgba(25,181,254,0.8)' #Blue
                
            elif i == 'Burnley':
                dict['team'] = i
                dict['colour'] = 'rgba(145,61,136,0.8)' #Plum Purple 
                
            elif i == 'Chelsea':
                dict['team'] = i
                dict['colour'] = 'rgba(0,0,255,0.8)' #Blue
                
            elif i == 'Crystal Palace':
                dict['team'] = i
                dict['colour'] = 'rgba(142,68,173,0.8)' #Purple
                
            elif i == 'Everton':
                dict['team'] = i
                dict['colour'] = 'rgba(40,90,255,0.8)' #Blue 
                
            elif i == 'Fulham':
                dict['team'] = i
                dict['colour'] = 'rgba(192,192,192,0.8)' #Grey
                
            elif i == 'Leeds':
                dict['team'] = i
                dict['colour'] = 'rgba(251,251,249,0.8)' #White
                
            elif i == 'Leicester':
                dict['team'] = i
                dict['colour'] = 'rgba(45,0,255,0.8)' #Blue
                
            elif i == 'Liverpool':
                dict['team'] = i
                dict['colour'] = 'rgba(255,0,0,0.8)' #Red
                
            elif i == 'Manchester City':
                dict['team'] = i
                dict['colour'] = 'rgba(34,167,240,0.8)' #Blue
                
            elif i == 'Manchester United':
                dict['team'] = i
                dict['colour'] = 'rgba(255,35,0,0.8)' #Red 
                
            elif i == 'Newcastle United':
                dict['team'] = i
                dict['colour'] = 'rgba(0,0,0,0.8)' #Black
                
            elif i == 'Sheffield United':
                dict['team'] = i
                dict['colour'] = 'rgba(207,0,15,0.8)' #Red
                
            elif i == 'Southampton':
                dict['team'] = i
                dict['colour'] = 'rgba(246,71,71,0.8)' #Red
                
            elif i == 'Tottenham':
                dict['team'] = i
                dict['colour'] = 'rgba(251,251,249,0.8)' #White
                
            elif i == 'West Bromwich Albion':
                dict['team'] = i
                dict['colour'] = 'rgba(1,50,67,0.8)' #Navy
                
            elif i == 'West Ham':
                dict['team'] = i
                dict['colour'] = 'rgba(145,61,136,0.8)' #Plum Purple
                
            elif i == 'Wolverhampton Wanderers':
                dict['team'] = i
                dict['colour'] = 'rgba(248,148,6,1)' #Orange
            
            results.append(dict)
        return results
