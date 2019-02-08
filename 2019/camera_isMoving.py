def isMoving(img):
    black_cnt = np.sum(img == 0)
    white_cnt = img.size - black_cnt
    #print("white:", white_cnt)
    #print("black:", black_cnt)
    if black_cnt > white_cnt:
        return False
    else:
        return True
