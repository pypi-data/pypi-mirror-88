from freehub import git_ops,Repo
import os
import json

def get_full_git_uri(git_uri,git_username,git_password):
    if git_uri.startswith('https://'):
        protocal='https'
    else:
        protocal='http'
    git_uri=git_uri.lstrip('http://').lstrip('https://')
    git_uri='%s://%s:%s@%s'%(protocal,git_username,git_password,git_uri)
    return git_uri

class T:
    class NOT_GIVEN:
        pass
class PointDict(dict):

    __no_value__ = '<__no_value__>'

    def __getattr__(self, key, default=T.NOT_GIVEN):
        if key in self.keys():
            return self[key]
        elif default != T.NOT_GIVEN:
            return default
        raise KeyError('No such key named %s' % (key))

    def __setattr__(self, key, value):
        self[key] = value

    def __call__(self, key, value=__no_value__):
        if value is self.__no_value__:
            self[key] = PointDict()
        else:
            self[key] = value
        return self[key]

    def set_attribute(self, key, value):
        self.__dict__[key] = value

    def get_attribute(self, *args, **kwargs):
        return self.__dict__.get(*args, **kwargs)

    def seta(self, **kwargs):
        for k, v in kwargs.items():
            self.set_attribute('__%s__' % (k), v)

    def geta(self, key, *args, **kwargs):
        return self.get_attribute('__%s__' % (key), *args, **kwargs)

    @classmethod
    def from_dict(cls, dic):
        dic2 = cls()
        for k, v in dic.items():
            if not isinstance(v, dict):
                dic2[k] = v
            else:
                dic2[k] = cls.from_dict(v)
        return dic2

    def print(self):
        import json
        print(json.dumps(self, sort_keys=True, indent=4))

    def print1(self, depth=0, step=5, space_around_delimiter=1, fillchar=' ', cell_border='|', delimiter=':'):
        import re
        def len_zh(data):
            temp = re.findall('[^a-zA-Z0-9.]+', data)
            count = 0
            for i in temp:
                count += len(i)
            return (count)

        for k, v in self.items():
            for i in range(depth):
                print(fillchar * step, end='')
                print(cell_border, end='')
            print(k.rjust(step - len_zh(k), fillchar),
                  end=' ' * space_around_delimiter + delimiter + ' ' * space_around_delimiter)
            if not isinstance(v, PointDict):
                print(v)
            else:
                print('\n', end='')
                v.print1(depth=depth + 1, step=step, space_around_delimiter=space_around_delimiter,
                         cell_border=cell_border, fillchar=fillchar, delimiter=delimiter)

    def pprint1(self):
        self.print1(step=5, space_around_delimiter=0, fillchar='`', cell_border='|', delimiter=':')
def load_json(path):
    with open(path,'r',encoding='utf-8') as f:
        return json.load(f)
def dump_json(data,path):
    with open(path,'w' ,encoding='utf-8') as f:
        return json.dump(data,f,ensure_ascii=False,indent=2)

def load_config(path):
    data=load_json(path)
    dic={}
    for k,v in data.items():
        if isinstance(v,dict):
            if 'value' in v.keys():
                v=v['value']
            else:
                v=v['default']
        dic[k]=v
    return PointDict.from_dict(dic)
def write_config(data,path):
    return dump_json(dict(**data),path)




def clone_repo(cfg):
    full_git_uri=get_full_git_uri(cfg.GIT_URI,cfg.GIT_USERNAME,cfg.GIT_PASSWORD)
    git_ops.clone_remote_repo(full_git_uri,cfg.DATA_DIR)

def sync_repo(cfg):
    full_git_uri = get_full_git_uri(cfg.GIT_URI, cfg.GIT_USERNAME, cfg.GIT_PASSWORD)
    if not os.path.exists(cfg.DATA_DIR):
        os.makedirs(cfg.DATA_DIR)
    if git_ops.is_git_repo(cfg.DATA_DIR):
        repo=Repo(cfg.DATA_DIR)
    else:
        repo=Repo.init(cfg.DATA_DIR)
    git_ops.pull_remote_branch(repo,full_git_uri,'master')