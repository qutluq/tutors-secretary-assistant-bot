import pandas as pd

class UserProfile():
    
    
    def __init__(self, id):
        '''user_profile = {"id":0,      "first_name":"", "last_name":"", 
                           "age":0,     "grade":0,
                           "email":"",  "phone":"",      "schedule":" e.g.[('09:00','пн')]"}
        '''
        
        self._filename = 'data/user_profiles.csv'
        self._df_user_profiles = pd.read_csv(self._filename, index_col='id')
        self._user_profile = {"id":id}

        if id in self._df_user_profiles.index.values:
            # update using data from database
            self._user_profile.update(self._df_user_profiles.loc[id].to_dict())
        else:
            # create empty profile
            self._user_profile.update({col:"" for col in self._df_user_profiles.columns})
            self._user_profile['age'] = self._user_profile['grade'] = 0 # use default values
            self._user_profile['schedule'] = '[]' # use default values
    
    def update(self, first_name="", last_name="", age=0, grade=0,
                     email="", phone="", schedule='[]', _att_name='', _att_value=''):
        
        user_profile = self._user_profile
        
        if first_name != "":
            user_profile["first_name"] = first_name

        if last_name != "":
            user_profile["last_name"] = last_name

        if age != 0:
            user_profile["age"] = age

        if grade != 0:
            user_profile["grade"] = grade

        if email != "":
            user_profile["email"] = email

        if phone != "":
            user_profile["phone"] = phone

        if schedule != '[]':
            user_profile["schedule"] = schedule
            
        if _att_name != "":
            user_profile[_att_name] = _att_value
            
            
    def _get_attribute_value(self, attribute_name):
        
        return self._user_profile[attribute_name]
        
    def get_id(self):
        
        return self._user_profile['id']

    def get_first_name(self):
        
        return self._user_profile['first_name']

    def get_last_name(self):
        
        return self._user_profile['last_name']

    def get_age(self):
        
        return self._user_profile['age']

    def get_grade(self):
        
        return self._user_profile['grade']

    def get_email(self):
        
        return self._user_profile['email']

    def get_phone(self):
        
        return self._user_profile['phone']

    def get_schedule(self):
        
        return self._user_profile['schedule']
    
    def get_attribute_names(self, exclude_schedule=False):
        
        types = {'first_name':str, 'last_name':str, 
                 'age':int, 'grade':int, 
                 'email':str, 'phone':str, 'schedule':str}

        excluded = ['id']
        if exclude_schedule:
            excluded.append('schedule')
            
        return [(key, types[key]) for key in self._user_profile.keys() if key not in excluded]
    
    def get_attribute_name_hf(self, att_name):
        '''get human-friendly attribute name'''
        
        names = {'first_name':'имя', 'last_name':'фамилия', 
                 'age':'возраст', 'grade':'класс', 
                 'email':'email', 'phone':'телефонный номер', 'schedule':'график'}
        
        return names[att_name]
    
    def contact_info_set(self):

        return (self.get_phone() != "") or (self.get_email() != "")

    def save(self):
        
        '''save user_profiles to disk'''
        user_profiles = self._df_user_profiles
        user_profile  = self._user_profile
        
        # update user's profile in database table
        user_profiles.loc[user_profile['id']] = pd.Series({k:v for k,v in user_profile.items() if k!='id'})
        user_profiles.to_csv(self._filename)