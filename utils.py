#coding: utf-8

def team_assign(aochd_team_str):
  players = _get_players(aochd_team_str)
  team1, team2 = _team_assign(players)
  aochd_str = _make_aochd_string(team1, team2)
  return aochd_str

# 10進数x（自然数）をn進数(2 ≦ n ≦ 16)に変換する関数
def convert_natural_radix_10_to_n(x, n):
  if x < 0: return None
  if n < 2 or 16 < n: return None
  if x == 0: return 0
  nchar = '0123456789ABCDEF'
  digit = 0
  result = ''
  while x > 0:
    result = nchar[x % n] + result
    x = int(x / n)
  return result

# 任意の人数でチーム分け。8人未満対応
def _team_assign(players):
  population = len(players) # 参加人数

  #奇数の場合は人数の多い方を理想レートに近づける
  num_of_digits = population - int(population / 2.0)

  rates = [player[1] for player in players]
  ideal = sum(rates) / 2.0 # 総和の1/2が理想とする
  idx_and_IdealDegree = [] # 組み合わせごとの理想度をメモするリスト

  # 「参加人数」進数で「チーム1の人数」桁まで考えればよい
  # 8人で4人チームなら、0000から7777までのrange
  # それぞれの桁の数は、ratesのindex
  # 参加者が奇数なら、人数の多い方がチーム1
  for i in range(population**num_of_digits):
    some_idx = [int(s) for s in str(convert_natural_radix_10_to_n(i, population)).rjust(num_of_digits, "0")]
    # そのうち同じ人が同じチームに二度以上入る組み合わせを取り除く
    idx_one_by_one = list(set(some_idx))
    if len(idx_one_by_one) == num_of_digits:
      # 理想との差を理想度とする
      ideal_degree = abs(ideal - sum([rates[idx] for idx in idx_one_by_one]))
      idx_and_IdealDegree.append((idx_one_by_one, ideal_degree))
  # 理想との差が少ない順にソート
  idx_and_IdealDegree.sort(key=lambda tuple_of_idx_and_IdealDigree: tuple_of_idx_and_IdealDigree[1])
  most_ideally_combination_idx = idx_and_IdealDegree[0][0]

  # pop()で要素を取り出すとindexが切り詰められるので、末尾からpop()する
  mici = sorted(most_ideally_combination_idx, reverse=True)

  team1 = [players.pop(idx) for idx in mici]
  team2 = players

  # レート高い順でソート
  team1.sort(key=lambda player: player[1], reverse=True)
  team2.sort(key=lambda player: player[1], reverse=True)

  return team1, team2

def _make_aochd_string(team1, team2):
  l = []
  l.append(u"チーム1:")
  l.append(u"【%s】" % sum([player[1] for player in team1]))
  for player in team1:
    l.append(u"%s(%s)" % player)
  l.append(u"チーム2:")
  l.append(u"【%s】" % sum([player[1] for player in team2]))
  for player in team2:
    l.append(u"%s(%s)" % player)
  return u" ".join(l)

def _get_players(aochd_team_str):
  players = []
  for s in aochd_team_str.split():
    if "(" in s:
      name = s.split("(")[0]
      rate = int(s.split("(")[1].split(")")[0])
      players.append((name, rate))
  return players
