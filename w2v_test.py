import pandas as pd
import numpy as np

class CareerMap():
    def __init__(self, df, jobColumn):
        self.jobCol = df[jobColumn]
        self.w2v = df 
        self.vecs = df.drop([jobColumn], axis=1)

    # Index the dataframe for the series representing the 
    def getPoint(self, index=None, title=None):
        assert index or title, "Index or Title must be given"
        
        if index:
            return pd.Series(self.vecs.iloc[index].values[0])

        if title:
            return pd.Series(self.vecs[ self.jobCol == title ].values[0])

    # Add vectors together
    def addIndices(self, a_index, b_index):
        a = self.getPoint(a_index)
        b = self.getPoint(b_index)
        return a.add(b)

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

    def combJob(self, titles, exclude=None, approx=True):
        # Grab the indices of all titles fiven
        i_list = self.w2v[ self.jobCol.isin(titles) ].index.values

        # Exclude things if necessary
        if exclude:
            assert isinstance(exclude, list), "Exclusion titles must be in a list"
            e_list = self.w2v[ self.jobCol.isin(exclude) ].index.values
        else:
            e_list = None

        # Average the coordinates corresponding to those indices
        average = self.avg(i_list)
        # Find the closest point to the average
        if approx:
            newPoint = self.findClosest(average, e_list)
            # Return the job title
            return newPoint['posTitle']
        return average

    # A is to B as C is to __
    def analogy(self, a, b, c, approx=True):
        # Make sure titles exist
        assert np.any(self.jobCol == a), f"{a} is not in the career map"
        assert np.any(self.jobCol == b), f"{b} is not in the career map"
        assert np.any(self.jobCol == c), f"{c} is not in the career map"
        # Replace job titles with indices
        a = self.getPoint(title=a)
        b = self.getPoint(title=b)
        c = self.getPoint(title=c)

        point = b.add(-a)
        point = point.add(c)
        # Find closest point
        if approx:
            point = self.findClosest(point)
            # Return the title
            return point['posTitle']
        
        # Otherwise, just return the point
        return point

    # |u|*|v|*cos = a.b
    def cosSim(self, a, b):
        # Norms
        a_norm = np.linalg.norm(a.values)
        b_norm = np.linalg.norm(b.values)
        # Calculations
        dot_product = a.dot(b)
        calc = dot_product/a_norm/b_norm
        return calc

if __name__ == '__main__':
    # Create the word2vec map
    w2v = pd.read_json('pos_w2v_matrix.json')
    cMap = CareerMap(w2v, 'posTitle')

    # Start using it!
    # job = cMap.combJob(['Engineer', 'Developer', '.NET Developer', 'Senior Developer'])
    # job = cMap.combJob(['Engineer','Senior'])
    job = cMap.analogy('Junior Engineer', 'Senior Engineer', 'Junior Developer', approx=False)

    dot = cMap.getPoint(title='.')
    sD = cMap.getPoint(title='Senior Developer')

    print('dot:', cMap.cosSim(job, dot))
    print('sD:', cMap.cosSim(job, sD))

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
