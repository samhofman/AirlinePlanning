\ Model MaxExample
\ LP format - for model browsing. Use MPS format to capture full model detail.
Minimize
  75 f_0,0 + 30 f_1,0 + 40 f_1,1 + 70 f_2,0 + 70 f_2,1 + 25 f_3,0 + 45 f_3,1
   + 0 s_0 + 0 s_1 + 0 s_2 + 0 s_3 + 0 s_4 + 1000 s_5 + 0 s_6
Subject To
 R0: 15 f_0,0 + 5 f_1,1 <= 20
 R1: 5 f_1,0 <= 10
 R2: 10 f_2,0 + 5 f_3,1 <= 10
 R3: 15 f_0,0 + 5 f_1,1 + 10 f_2,1 + 5 f_3,1 <= 20
 R4: <= 40
 R5: 5 f_1,0 + 10 f_2,0 + 5 f_3,0 - s_5 <= 10
 R6: 5 f_1,1 + 10 f_2,1 + 5 f_3,1 <= 30
 R7: f_0,0 = 1
 R8: f_1,0 + f_1,1 = 1
 R9: f_2,0 + f_2,1 = 1
 R10: f_3,0 + f_3,1 = 1
Bounds
End
