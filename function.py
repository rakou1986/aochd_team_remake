def _team_assign(self, general_record):
  """任意の人数をチーム分け"""

  # 10進数（自然数）をn進数に変換する関数。拾い物。動作確認済み
  def convert_natural_radix_10_to_n(x, n):
    if x < 0: return None
    if n < 2 or 16 < n: return None
    if x == 0: return 0
    nchar = '0123456789ABCDEF'
    digit = 0
    result = ''
    while x > 0:
      result = nchar[x % n] + result
      x = x / n
    return result

  prs = self._get_inside_member_prs(general_record=general_record)
  pop = len(prs)
  num_of_digits = pop - int(pop / 2.0) #奇数の場合人数の多い方を理想レートに近づける
  rates = [pr.user.rate for pr in prs]
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
  team1 = [prs.pop(idx) for idx in mici]
  team2 = prs

  for pr in team1:
    pr.team = conf.TEAM1
  for pr in team2:
    pr.team = conf.TEAM2

  # チーム分け当時のレートを保存。勝敗による変動レート計算用。
  # これがないとゲーム中にレートが手動で修正されたとき、チームの合計レートが
  # 変わるせいで、勝敗によるレート変動に過不足が出る。
  for pr in team1 + team2:
    pr.rate_at_umari = pr.user.rate

  db_session.flush()
