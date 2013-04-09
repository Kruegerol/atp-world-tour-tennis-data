# Your input
player = "Roger-Federer"
turned_pro = 1998
final_year = 2012

# Imports
import urllib
from lxml import etree
import StringIO

# FUNCTIONS
# Unicode cleanup function
def ascii_replace(your_input):
  for x in xrange(0, len(your_input)):
    your_input[x] = your_input[x].encode('ascii', 'replace')
    your_input[x] = your_input[x].replace("?", " ")

# Match array function
def get_matches(index, html, tree):
  div_index = index + 2
  div_index_string = str(div_index)
  # Round
  xpath = "//div[" + div_index_string + "]/div/table/tbody/tr/td[1]/text()"
  test = tree.xpath(xpath)
  tournament_round = test
  tournament_round.pop(0)
  # Opponents
  html2 = html
  html2 = html2.replace("</a/>", "")
  html2 = html2.replace("</a>", "")
  html2 = html2.replace("<a href=", "")
  tree2 = etree.parse(StringIO.StringIO(html2), parser)
  xpath = "//div[" + div_index_string + "]/div/table/tbody/tr/td[2]/text()"
  test = tree2.xpath(xpath)
  ascii_replace(test)
  for j in xrange(0, len(test)):
    test[j] = test[j].replace("\r\n", "")
    index1 = test[j].find(">") + 1
    test[j] = test[j][index1:]
    test[j] = test[j].strip(" ")
  opponents = test
  opponents.pop(0)
  # Ranking
  xpath = "//div[" + div_index_string + "]/div/table/tbody/tr/td[3]/text()"
  test = tree.xpath(xpath)
  for x in xrange(0, len(test)):
    test[x] = test[x].replace("\r\n", "")
    test[x] = test[x].strip(" ")
  opponent_ranking = test
  opponent_ranking.pop(0)
  # Score
  xpath = "//div[" + div_index_string + "]/div/table/tbody/tr/td[4]/text()"
  test = tree.xpath(xpath)
  ascii_replace(test)
  score = test
  score.pop(0)
  # Stats link
  xpath = "//div[" + div_index_string + "]/div/table/tbody/tr/td[5]/a/@onclick"
  test = tree.xpath(xpath)
  for x in xrange(0, len(test)):
    test[x] = test[x].replace("openWin('", "")
    index = test[x].find("'")
    test[x] = test[x][0:index]
    test[x] = "http://www.atpworldtour.com" + test[x]
  stats_link = test
  # Putting together the match array
  # "round", "opponent", "ranking", "score", "stats link"
  match_array = []
  for j in xrange(0, len(tournament_round)):
    match_array_row = [tournament_round[j], opponents[j], opponent_ranking[j], score[j], stats_link[j]]
    match_array.append(match_array_row)
  return match_array
# Final array header
final_array = [["year", "tournament", "start date", "type", "surface", "draw", "atp points", "atp ranking", "tournament prize money", "round", "opponent", "ranking", "score", "stats link", "tournament", "tournament_round", "time", "winner", "player1 name", "player1 nationality", "player 1 aces", "player1 double faults", "player1 1st serves in", "player1 1st serves total", "player1 1st serve points won", "player1 1st serve points total", "player1 2nd serve points won", "player1 2nd serve points total", "player1 break points won", "player1 break points total", "player1 service games played", "player1 1st serve return points won", "player1 1st serve return points total", "player1 2nd serve return points won", "player1 2nd serve return points total", "player1 break points converted won", "player1 break points converted total", "player1 return games played", "player1 total service points won", "player1 total service points total", "player1 total return points won", "player1 total return points total", "player1 total points won", "player1 total points total"]]

# Info1 [tournament, date, type, surface, draw]
def get_info1(html, tree):
  html2 = html
  html2 = html2.replace("<strong>", "")
  html2 = html2.replace("</strong>", "")
  html2 = html2.replace("</a/>", "")
  html2 = html2.replace("</a>", "")
  html2 = html2.replace("<a href=", "")
  tree = etree.parse(StringIO.StringIO(html2), parser)
  xpath = "//div[2]/div[2]/div/div/p/text()"
  test = tree.xpath(xpath)
  ascii_replace(test)
  for x in xrange(0, len(test)):
    index = test[x].find(">") + 1
    test[x] = test[x][index:]
    test[x] = test[x].replace("\r\n\t", "")
    test[x] = test[x].split("; ")
  info1 = test
  return info1

# Info2 [null, points, ranking, prize money]
def get_info2(tree):
  xpath = "//div[2]/div/div/p/span/text()"
  test = tree.xpath(xpath)
  ascii_replace(test)
  for x in xrange(0, len(test)):
    test[x] = test[x].split(":")
    test[x][1] = test[x][1].replace(", ATP Ranking", "")
    test[x][1] = test[x][1].strip(" ")
    test[x][2] = test[x][2].replace(", Prize Money", "")
    test[x][2] = test[x][2].strip(" ")
    test[x][3] = test[x][3].strip(" ")
  info2 = test
  return info2

# Match stats function
def match_stats(match_url, html):
  result = urllib.urlopen(match_url)
  html = result.read()
  parser = etree.HTMLParser()
  tree   = etree.parse(StringIO.StringIO(html), parser)
  xpath1 = "//tr[3]/td/a/text()"
  tournament = tree.xpath(xpath1)[0]
  xpath2 = "//tr[5]/td/text()"
  tournament_round = tree.xpath(xpath2)[0]
  xpath3 = "//tr[7]/td/text()"
  time = tree.xpath(xpath3)[0]
  time = time.encode('ascii', 'ignore')
  time = time.replace("minutes", "")
  xpath4 = "//tr[9]/td/a/text()"
  winner = tree.xpath(xpath4)[0]
  xpath5 = "//tr[11]/td/a/text()"
  player1_name = tree.xpath(xpath5)[0]
  player2_name = tree.xpath(xpath5)[1]
  xpath7 = "//p/text()"
  player1_nationality = tree.xpath(xpath7)[0]
  try:
    player2_nationality = tree.xpath(xpath7)[1]
  except Exception:
    player2_nationality = ""  
  xpath8 = "//td/text()"
  match_stats_array = tree.xpath(xpath8)
  player1_aces = match_stats_array[13]
  player2_aces = match_stats_array[14]
  player1_double_faults = match_stats_array[16]
  player2_double_faults = match_stats_array[17]
  def cleanup(your_input):
    temp = your_input
    temp = temp.encode('ascii', 'ignore')
    index1 = temp.find("%") + 1
    temp = temp[index1:]
    temp = temp.replace("(", "")
    temp = temp.replace(")", "")
    temp = temp.split("/")
    return temp
  # 1st serve
  player1_1st_serves = match_stats_array[19]
  player1_1st_serves = cleanup(player1_1st_serves)
  player1_1st_serves_in = player1_1st_serves[0]
  player1_1st_serves_total = player1_1st_serves[1]
  player2_1st_serves = match_stats_array[20]
  player2_1st_serves = cleanup(player2_1st_serves)
  player2_1st_serves_in = player2_1st_serves[0]
  player2_1st_serves_total = player2_1st_serves[1]
  # 1st serve points won
  player1_1st_serves_won = match_stats_array[22]
  player1_1st_serves_won = cleanup(player1_1st_serves_won)
  player1_1st_serve_points_won = player1_1st_serves_won[0]
  player1_1st_serve_points_total = player1_1st_serves_won[1]
  player2_1st_serves_won = match_stats_array[23]
  player2_1st_serves_won = cleanup(player2_1st_serves_won)
  player2_1st_serve_points_won = player2_1st_serves_won[0]
  player2_1st_serve_points_total = player2_1st_serves_won[1]
  # 2nd serve points won
  player1_2nd_serves_won = match_stats_array[25]
  player1_2nd_serves_won = cleanup(player1_2nd_serves_won)
  player1_2nd_serve_points_won = player1_2nd_serves_won[0]
  player1_2nd_serve_points_total = player1_2nd_serves_won[1]
  player2_2nd_serves_won = match_stats_array[26]
  player2_2nd_serves_won = cleanup(player2_2nd_serves_won)
  player2_2nd_serve_points_won = player2_2nd_serves_won[0]
  player2_2nd_serve_points_total = player2_2nd_serves_won[1]
  # Break points saved
  player1_break_points = match_stats_array[28]
  player1_break_points = cleanup(player1_break_points)
  player1_break_points_won = player1_break_points[0]
  player1_break_points_total = player1_break_points[1]
  player2_break_points = match_stats_array[29]
  player2_break_points = cleanup(player2_break_points)
  player2_break_points_won = player2_break_points[0]
  player2_break_points_total = player2_break_points[1]
  # Service games played
  player1_service_games_played = match_stats_array[31]
  player2_service_games_played = match_stats_array[32]
  # 1st serve return points won
  player1_1st_serve_return_points = match_stats_array[34]
  player1_1st_serve_return_points = cleanup(player1_1st_serve_return_points)
  player1_1st_serve_return_points_won = player1_1st_serve_return_points[0]
  player1_1st_serve_return_points_total = player1_1st_serve_return_points[1]
  player2_1st_serve_return_points = match_stats_array[35]
  player2_1st_serve_return_points = cleanup(player2_1st_serve_return_points)
  player2_1st_serve_return_points_won = player2_1st_serve_return_points[0]
  player2_1st_serve_return_points_total = player2_1st_serve_return_points[1]
  # 2nd serve return points won
  player1_2nd_serve_return_points = match_stats_array[37]
  player1_2nd_serve_return_points = cleanup(player1_2nd_serve_return_points)
  player1_2nd_serve_return_points_won = player1_2nd_serve_return_points[0]
  player1_2nd_serve_return_points_total = player1_2nd_serve_return_points[1]
  player2_2nd_serve_return_points = match_stats_array[38]
  player2_2nd_serve_return_points = cleanup(player2_2nd_serve_return_points)
  player2_2nd_serve_return_points_won = player2_2nd_serve_return_points[0]
  player2_2nd_serve_return_points_total = player2_2nd_serve_return_points[1]
  # Break points converted
  player1_break_points_converted = match_stats_array[40]
  player1_break_points_converted = cleanup(player1_break_points_converted)
  player1_break_points_converted_won = player1_break_points_converted[0]
  player1_break_points_converted_total = player1_break_points_converted[1]
  player2_break_points_converted = match_stats_array[41]
  player2_break_points_converted = cleanup(player2_break_points_converted)
  player2_break_points_converted_won = player2_break_points_converted[0]
  player2_break_points_converted_total = player2_break_points_converted[1]
  # Return games played
  player1_return_games_played = match_stats_array[43]
  player2_return_games_played = match_stats_array[44]
  # Total service points won
  player1_total_service_points = match_stats_array[46]
  player1_total_service_points = cleanup(player1_total_service_points)
  player1_total_service_points_won = player1_total_service_points[0]
  player1_total_service_points_total = player1_total_service_points[1]
  player2_total_service_points = match_stats_array[47]
  player2_total_service_points = cleanup(player2_total_service_points)
  player2_total_service_points_won = player2_total_service_points[0]
  player2_total_service_points_total = player2_total_service_points[1]
  # Total return points won
  player1_total_return_points = match_stats_array[49]
  player1_total_return_points = cleanup(player1_total_return_points)
  player1_total_return_points_won = player1_total_return_points[0]
  player1_total_return_points_total = player1_total_return_points[1]
  player2_total_return_points = match_stats_array[50]
  player2_total_return_points = cleanup(player2_total_return_points)
  player2_total_return_points_won = player2_total_return_points[0]
  player2_total_return_points_total = player2_total_return_points[1]
  # Total points won
  player1_total_points = match_stats_array[52]
  player1_total_points = cleanup(player1_total_points)
  player1_total_points_won = player1_total_points[0]
  player1_total_points_total = player1_total_points[1]
  player2_total_points = match_stats_array[53]
  player2_total_points = cleanup(player2_total_points)
  player2_total_points_won = player2_total_points[0]
  player2_total_points_total = player2_total_points[1]
  # Player arrays
  player1_array = [tournament, tournament_round, time, winner, player1_name, player1_nationality, player1_aces, player1_double_faults, player1_1st_serves_in, player1_1st_serves_total, player1_1st_serve_points_won, player1_1st_serve_points_total, player1_2nd_serve_points_won, player1_2nd_serve_points_total, player1_break_points_won, player1_break_points_total, player1_service_games_played, player1_1st_serve_return_points_won, player1_1st_serve_return_points_total, player1_2nd_serve_return_points_won, player1_2nd_serve_return_points_total, player1_break_points_converted_won, player1_break_points_converted_total, player1_return_games_played, player1_total_service_points_won, player1_total_service_points_total, player1_total_return_points_won, player1_total_return_points_total, player1_total_points_won, player1_total_points_total, player2_name, player2_nationality, player2_aces, player2_double_faults, player2_1st_serves_in, player2_1st_serves_total, player2_1st_serve_points_won, player2_1st_serve_points_total, player2_2nd_serve_points_won, player2_2nd_serve_points_total, player2_break_points_won, player2_break_points_total, player2_service_games_played, player2_1st_serve_return_points_won, player2_1st_serve_return_points_total, player2_2nd_serve_return_points_won, player2_2nd_serve_return_points_total, player2_break_points_converted_won, player2_break_points_converted_total, player2_return_games_played, player2_total_service_points_won, player2_total_service_points_total, player2_total_return_points_won, player2_total_return_points_total, player2_total_points_won, player2_total_points_total]  
  return player1_array


# List of years
years_list = []
difference = final_year - turned_pro + 1
for x in xrange(0, difference):
  temp = x + turned_pro
  years_list.append(temp)
  
# Final array: Getting all the data
final_array = []
for row in years_list:
  year = row  
  # Initial reading in the URL
  year_string = str(year)
  url = "http://www.atpworldtour.com/Tennis/Players/Top-Players/" + player + ".aspx?t=pa&y=" + year_string + "&m=s&e=0#"
  result = urllib.urlopen(url)
  html = result.read()
  parser = etree.HTMLParser()
  tree = etree.parse(StringIO.StringIO(html), parser)
  # Pre-array 1 (using the functions)
  array1 = []
  for i in xrange(0, len(get_info1(html, tree))):
    array1_row = [get_info1(html, tree)[i][0], get_info1(html, tree)[i][1], get_info1(html, tree)[i][2], get_info1(html, tree)[i][3], get_info1(html, tree)[i][4], get_info2(tree)[i][1], get_info2(tree)[i][2], get_info2(tree)[i][3], get_matches(i, html, tree)]
    array1.append(array1_row)
  # Pre-array 2
  array2 = []
  for i in xrange(0, len(array1)):
    for j in xrange(0, len(array1[i][8])):
      array2_row = [year, array1[i][0], array1[i][1], array1[i][2], array1[i][3], array1[i][4], array1[i][5], array1[i][6], array1[i][7], array1[i][8][j][0], array1[i][8][j][1], array1[i][8][j][2], array1[i][8][j][3], array1[i][8][j][4]]
      array2.append(array2_row)
  # Match stats array
  match_stats_array = []
  for i in xrange(0, len(array2)):
    match_url = array2[i][13]
    row_array = match_stats(match_url, html)
    match_stats_array.append(row_array)
  # Final array
  final_year_array = [array2[ix] + match_stats_array[ix] for ix in range(len(array2))]
  final_array.append(final_year_array)

# Output array
output_array = final_array[0]
for i in xrange(1, len(final_array)):
  output_array = output_array + final_array[i]

# Add the CSV headers
headers = [["year", "tournament", "start date", "type", "surface", "draw", "atp points", "atp ranking", "tournament prize money", "round", "opponent", "ranking", "score", "stats link", "tournament", "tournament round", "time", "winner", "player1 name", "player1 nationality", "player1 aces", "player1 double faults", "player1 1st serves in", "player1 1st serves total", "player1 1st serve points won", "player1 1st serve points total", "player1 2nd serve points won", "player1 2nd serve points total", "player1 break points won", "player1 break points total", "player1 service games played", "player1 1st serve return points won", "player1 1st serve return points total", "player1 2nd serve return points won", "player1 2nd serve return points total", "player1 break points converted won", "player1 break points converted total", "player1 return games played", "player1 total service points won", "player1 total service points total", "player1 total return points won", "player1 total return points total", "player1 total points won", "player1 total points total", "player2 name", "player2 nationality", "player2 aces", "player2 double faults", "player2 1st serves in", "player2 1st serves total", "player2 1st serve points won", "player2 1st serve points total", "player2 2nd serve points won", "player2 2nd serve points total", "player2 break points won", "player2 break points total", "player2 service games played", "player2 1st serve return points won", "player2 1st serve return points total", "player2 2nd serve return points won", "player2 2nd serve return points total", "player2 break points converted won", "player2 break points converted total", "player2 return games played", "player2 total service points won", "player2 total service points total", "player2 total return points won", "player2 total return points total", "player2 total points won", "player2 total points total"]]

output_array = headers + output_array

# CSV output
import csv
csv_out = open(player + ".csv", 'wb')
mywriter = csv.writer(csv_out)
for row in output_array:
  mywriter.writerow(row)
csv_out.close()