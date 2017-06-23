#coding: utf-8

def team_assign(aochd_team_str):
  players = _get_players(aochd_team_str)
  team1, team2 = _team_assign(players)
  aochd_str = _make_aochd_string(team1, team2)
  return aochd_str

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

# 10進数x（自然数）をn進数に変換する関数。拾い物。動作確認済み
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

def _team_assign(players):
  pop = len(players)

  #奇数の場合人数の多い方を理想レートに近づける
  num_of_digits = pop - int(pop / 2.0)

  rates = [player[1] for player in players]
  ideal = sum(rates) / 2.0 # 総和の1/2が理想とする
  idx_and_IdealDegree = [] # 組み合わせごとの理想度をメモするリスト

  # pop進数のチーム人数桁まで考えればよい
  for i in range(pop**num_of_digits):
    some_idx = [int(s) for s in str(convert_natural_radix_10_to_n(i, pop)).rjust(num_of_digits, "0")]
    # そのうち同じ人が同じチームに二度以上入る組み合わせを取り除く
    idx_one_by_one = list(set(some_idx))
    if len(idx_one_by_one) == num_of_digits:
      # 理想との差を理想度とする
      ideal_degree = abs(ideal - sum([rates[idx] for idx in idx_one_by_one]))
      idx_and_IdealDegree.append((idx_one_by_one, ideal_degree))
  # 理想との差が少ない順にソート
  idx_and_IdealDegree.sort(key=lambda element: element[1])
  most_ideally_combination_idx = idx_and_IdealDegree[0][0]

  # pop()で要素を取り出すとindexが切り詰められるので、末尾からpop()する
  mici = sorted(most_ideally_combination_idx, reverse=True)

  team1 = [players.pop(idx) for idx in mici]
  team2 = players

  team1.sort(key=lambda player: player[1], reverse=True)
  team2.sort(key=lambda player: player[1], reverse=True)

  return team1, team2