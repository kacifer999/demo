# from cyai.settings.path import *
# from mmengine import Config, ConfigDict

# class ProjectsConfig(object):
#     def load_projects_config(self):
#         if not Path(PROJECTS_CONFIG_DIR).is_file():
#             Config(dict(projects=[])).dump(PROJECTS_CONFIG_DIR)
#         self.projects_config = Config.fromfile(PROJECTS_CONFIG_DIR)
#         self.projects = self.projects_config.projects
    
#     # def get_active(self):
#     #     for project in self.projects:
#     #         if project.status == 'active':
#     #             return project.name
#     #     return None


#     def set_inactive(self):
#         for project in self.projects:
#             if project.status == 'active':
#                 project.status = 'inactive'
    

#     def set_active(self, project_name):
#         for project in self.projects:
#             if project.name == project_name:
#                 project.status = 'active'
#                 break
        

#     def create(self, project_name):
#         self.set_inactive()
#         self.projects.append(ConfigDict({"name": project_name, "status": "active"}))
#         self.projects_config.dump(PROJECTS_CONFIG_DIR)
    

#     # def switch(self, project_name):
#     #     self.set_inactive()
#     #     self.set_active(project_name)
#     #     self.projects_config.dump(PROJECTS_CONFIG_DIR)
    
#     def delete(self, project_name):
#         for project in self.projects:
#             if project.name == project_name:
#                 self.projects.remove(project)
#                 break
#         if len(self.projects) > 0:
#             self.projects[0].status = "active"
#         self.projects_config.dump(PROJECTS_CONFIG_DIR)    




