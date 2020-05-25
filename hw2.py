def printCompetitor(competitor):
    '''
    Given the data of a competitor, the function prints it in a specific format.
    Arguments:
        competitor: {'competition name': competition_name, 'competition type': competition_type,
                        'competitor id': competitor_id, 'competitor country': competitor_country, 
                        'result': result}
    '''
    competition_name = competitor['competition name']
    competition_type = competitor['competition type']
    competitor_id = competitor['competitor id']
    competitor_country = competitor['competitor country']
    result = competitor['result']
    
    assert(isinstance(result, int)) # Updated. Safety check for the type of result

    print(f'Competitor {competitor_id} from {competitor_country} participated in {competition_name} ({competition_type}) and scored {result}')


def printCompetitionResults(competition_name, winning_gold_country, winning_silver_country, winning_bronze_country):
    '''
    Given a competition name and its champs countries, the function prints the winning countries 
        in that competition in a specific format.
    Arguments:
        competition_name: the competition name
        winning_gold_country, winning_silver_country, winning_bronze_country: the champs countries
    '''
    undef_country = 'undef_country'
    countries = [country for country in [winning_gold_country, winning_silver_country, winning_bronze_country] if country != undef_country]
    print(f'The winning competitors in {competition_name} are from: {countries}')


def key_sort_competitor(competitor):
    '''
    A helper function that creates a special key for sorting competitors.
    Arguments:
        competitor: a dictionary contains the data of a competitor in the following format: 
                    {'competition name': competition_name, 'competition type': competition_type,
                        'competitor id': competitor_id, 'competitor country': competitor_country, 
                        'result': result}
    '''
    competition_name = competitor['competition name']
    result = competitor['result']
    return (competition_name, result)


def readParseData(file_name):
    '''
    Given a file name, the function returns a list of competitors.
    Arguments: 
        file_name: the input file name. Assume that the input file is in the directory of this script.
    Return value:
        A list of competitors, such that every record is a dictionary, in the following format:
            {'competition name': competition_name, 'competition type': competition_type,
                'competitor id': competitor_id, 'competitor country': competitor_country, 
                'result': result}
    '''
    competitors_in_competitions = []
    competition_labels = ['competition name', 'competition type', 'competitor id', 'competitor country', 'result']

    # read the text file into a list
    with open(file_name, 'r') as f:
        text_lines = f.readlines()
    competitors = []
    competitions = []
    # iterates over the lines and creates list following the first word in the line
    for line in text_lines:
        line = line[:-1]
        line_words = line.split(' ')
        if(line_words[0] == 'competitor'):
            competitors.append([line_words[i] for i in range(1,len(line_words))])
        else:
            competitions.append([line_words[i] for i in range(1,len(line_words))])
    # ordering the list of dictionaries 
    for competitor in competitors:
        for competition in competitions:
            if (competitor[0] == competition[1]):
                # orders the labels by the right order
                ordered_list = [competition[0], competition[2], int(competition[1]), competitor[1], int(competition[3])]
                competitors_in_competitions.append({key:value for (key,value) in zip(competition_labels, ordered_list)})
    return competitors_in_competitions

# if competitor shows more then one time return false
def checkSingleParticipation(competitors_in_competitions, competition_name, competitor_id):
    counter = 0
    for competition in competitors_in_competitions:
        if competition['competition name'] == competition_name and competition['competitor id'] == competitor_id:
            counter += 1
    if counter > 1:
        return False
    return True

# creates a new legal competitors list if needed
def createLegalParticipantsList(competitors_in_competitions):
    new_participants_list = [competition for competition in competitors_in_competitions if 
    checkSingleParticipation(competitors_in_competitions, competition['competition name'],
                             competition['competitor id'])]
    return new_participants_list

# best result in comp knockout/timed
def calcWinningCountries(competition_name, competitors_in_competitions, lowest = True):
    winning_list = [competition_name, 'undef_country', 'undef_country', 'undef_country']
    countries = []
    results = []
    for element in competitors_in_competitions:
        if element['competition name'] == competition_name:
            countries.append(element['competitor country'])
            results.append(element['result'])
    for i in range(3):
        if countries:
            if (lowest is True):
                minimum = min(results)
                min_index = results.index(minimum)
                winning_list[i+1] = countries.pop(min_index)
                results.remove(minimum)
            elif (lowest is False):
                maximum = max(results)
                max_index = results.index(maximum)
                winning_list[i+1] = countries.pop(max_index)
                results.remove(maximum)
    return winning_list
            
def checkBestResult(competition_name, competition_type, competitors_in_competitions):
    if (competition_type == 'timed' or competition_type == 'knockout'):
        return calcWinningCountries(competition_name, competitors_in_competitions)
    else:
        return calcWinningCountries(competition_name, competitors_in_competitions, False)

def calcCompetitionsResults(competitors_in_competitions):
    '''
    Given the data of the competitors, the function returns the champs countries for each competition.
    Arguments:
        competitors_in_competitions: A list that contains the data of the competitors
                                    (see readParseData return value for more info)
    Retuen value:
        A list of competitions and their champs (list of lists). 
        Every record in the list contains the competition name and the champs, in the following format:
        [competition_name, winning_gold_country, winning_silver_country, winning_bronze_country]
    '''
    competitions_champs = []
    corrected_list = createLegalParticipantsList(competitors_in_competitions)
    alreadyBeen = []
    for competition in corrected_list:
        if competition['competition name'] not in alreadyBeen:
            competitions_champs.append(
                checkBestResult(competition['competition name'], competition['competition type'], corrected_list))
            alreadyBeen.append(competition['competition name'])

    # TODO Part A, Task 3.5
    
    return competitions_champs


def partA(file_name = 'input.txt', allow_prints = True):
    # read and parse the input file
    competitors_in_competitions = readParseData(file_name)
    if allow_prints:
        # competitors_in_competitions are sorted by competition_name (string) and then by result (int)
        for competitor in sorted(competitors_in_competitions, key=key_sort_competitor):
            printCompetitor(competitor)
    
    # calculate competition results
    competitions_results = calcCompetitionsResults(competitors_in_competitions)
    if allow_prints:
        for competition_result_single in sorted(competitions_results):
            printCompetitionResults(*competition_result_single)
    
    return competitions_results


def partB(file_name = 'input.txt'):
    import Olympics
    competitions_results = partA(file_name, allow_prints = False)
    olympics = Olympics.OlympicsCreate()
    for result in competitions_results:
        Olympics.OlympicsUpdateCompetitionResults(olympics, str(result[1]), str(result[2]), str(result[3]))
    Olympics.OlympicsWinningCountry(olympics)
    Olympics.OlympicsDestroy(olympics)
    # TODO Part B


if __name__ == "__main__":
    '''
    The main part of the script.
    __main__ is the name of the scope in which top-level code executes.
    
    To run only a single part, comment the line below which correspondes to the part you don't want to run.
    '''    
    file_name = 'input.txt'

    partA(file_name)
    partB(file_name)