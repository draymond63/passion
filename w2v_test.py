import pandas as pd
import numpy as np
from w2v_use import CareerMap

def testAnalogy(cm, a, b, c, d):
    guess = cm.analogy(a, b, c)
    # print(guess)
    return int(d == guess)

analogies = [
    # A                 B                   C                   D (Answer)
    ['Junior Developer', 'Senior Developer', 'Junior Engineer', 'Senior Engineer'],
    ['Junior Engineer', 'Senior Engineer', 'Junior Developer', 'Senior Developer'],
    ['CFO', 'CMO', 'Accountant', 'Doctor']
]

if __name__ == '__main__':
    # Create the word2vec map
    w2v = pd.read_json('pos_w2v_matrix.json')
    cMap = CareerMap(w2v, 'posTitle')
    # Keep track of how well we do
    score = 0
    for l in analogies:
        score += testAnalogy(cMap, *l)

    print('Score:', score*100/len(analogies), '%')

# 1                          .NET Developer
# 2                 .NET Software Developer
# 3                     .NET Technical Lead
# 4                          .Net Developer
# 5                           3D Generalist
# 6                3D Generalist / Designer
# 7                          AEM Consultant
# 8                      AEM Technical Lead
# 9                        AEM/CQ Developer
# 10                      ARC Future Fellow
# 11                      ASBAS Coordinator
# 12                       AV/IT Franchisee
# 13                               Academic
# 14                 Academic (part – time)
# 15                         Academic Tutor
# 16                  Academic and Research
# 17       Academic researcher and lecturer
# 18          Accident & Health Underwriter
# 19                    Account Coordinator
# 20               Account Delivery Manager
# 21                       Account Director
# 22     Account Director (Samsung Account)
# 23                       Account Engineer
# 24                      Account Executive
# 25                         Account Intern
# 26                        Account Manager
# 27                             Accountant
# 28                       Accounting Clerk
# 29                      Accounting Intern
# 30                     Accounting Officer
# 31                     Accounting Trainee
# 32                     Accounts Assistant
# 33                       Accounts Payable
# 34               Accounts Payable Officer
# 35         Accounts Receivable Specialist
# 36                             Acting CEO
# 37         Acting Chief Financial Officer
# 38                 Acting Finance Manager
# 39                  Acting Head of School
# 40                         Acting Manager
# 41    Acting Visitor Services Coordinator
# 42                                  Actor
# 43              Actor / Simulated Patient
# 44                      Actuarial Analyst
# 45            Adjunct Associate Professor
# 46                        Adjunct Faculty
# 47                         Adjunct Fellow
# 48                       Adjunct Lecturer
# 49                      Adjunct Professor
# 51                      Adjunct Senior Lecturer
# 52               Adjunct Senior Research Fellow
# 53                               Administration
# 54                     Administration Assistant
# 55                       Administration Manager
# 56                       Administration Officer
# 57                     Administrative Assistant
# 58                       Administrative Officer
# 59     Administrative and project officer roles
# 60                                Administrator
# 61                           Admissions Officer
# 62                   Advanced Financial Planner
# 63                Advanced Skills Teacher - ESL
# 64                    Advanced Sports Dietitian
# 65              Advertising Media Planner/Buyer
# 66                               Advice Manager
# 67                                      Adviser
# 68                                      Advisor
# 69                        Advisory Board Member
# 70                      Advisory Council Member
# 71                           Aerospace Engineer
# 72                       Agency Account Manager
# 73                       Agile Business Analyst
# 74                                  Agile Coach
# 75            Agile Delivery Coach (Consulting)
# 76                        Agile Project Manager
# 77                                 Agile Tester
# 78                         Agribusiness Analyst
# 79                         Agribusiness Manager
# 80                Aircraft Development Engineer
# 81                     Alliance Project Manager
# 82                           Altis - Consultant
# 83                        Altis - Delivery Lead
# 84                 Altis - Principal Consultant
# 85                         Altis - Project Lead
# 86                    Altis - Senior Consultant
# 87                     Alumni Relations Officer
# 88                                   Ambassador
# 89                                      Analyst
# 90                          Analyst (Analytics)
# 91                         Analyst / Programmer
# 92                            Analyst Developer
# 93                           Analyst Programmer
# 94                           Analyst/Programmer
# 95                           Analytical Chemist
# 96                         Analytics Consultant
# 97                            Analytics Manager
# 98                            Android Developer
# 99                            Android Team Lead
# 100                      Android Technical Lead
