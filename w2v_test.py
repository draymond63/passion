import pandas as pd
import numpy as np

class CareerMap():
    def __init__(self, df, jobColumn):
        self.jobCol = df[jobColumn]
        self.w2v = df 
        self.vecs = df.drop([jobColumn], axis=1)

    # Index the dataframe for the series representing the 
    def getPoint(self, index):
        return self.vecs.iloc[index]

    # Add vectors together
    def add(self, a_index, b_index):
        a = self.getPoint(a_index)
        b = self.getPoint(b_index)
        return a.add(b).tolist()

    # Take the centroid of a list of points
    def avg(self, i_list):
        vec_list = [0] * len(i_list)

        for i, index in enumerate(i_list):
            vec_list[i] = self.getPoint(index)

        df = pd.concat(vec_list, axis=1)
        return df.mean(axis=1)

    def findClosest(self, node, exclude=None):
        # Exclude points as necessary
        if exclude:
            df = self.vecs.drop(exclude)
        else:
            df = self.vecs
        # Compute the Euclidean distance
        dist_vect = np.sum((df - node)**2, axis=1)
        # Grab the lowest vector
        index = dist_vect.idxmin()
        # Return the point with the title
        return self.w2v.iloc[index]

    def combJob(self, titles, exclude=None):
        # try:
        # Grab the indices of all titles fiven
        i_list = self.w2v[ self.jobCol.isin(titles) ].index.values

        # Exclude things if necessary
        if exclude:
            assert isinstance(exclude, list), "Exclusion titles must be in a list"
            e_list = self.w2v[ self.jobCol.isin(exclude) ].index.values
        else:
            e_list = None
        # except:
        #     raise AssertionError("Title not found in dataset")

        # Average the coordinates corresponding to those indices
        average = self.avg(i_list)
        # Find the closest point to the average
        newPoint = self.findClosest(average, e_list)
        # Return the job title
        return newPoint['posTitle']

        

# Create the word2vec map
w2v = pd.read_json('pos_w2v_matrix.json')
cMap = CareerMap(w2v, 'posTitle')

# Start using it!
newJob = cMap.combJob(['Engineer', 'Developer', '.NET Developer', 'Senior Developer'])
newJob = cMap.combJob(['CEO', 'Senior Developer'])
print(newJob)


# print(cMap.w2v['posTitle'])
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
