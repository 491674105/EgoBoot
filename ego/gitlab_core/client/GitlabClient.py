from gitlab.const import SearchScope, AccessLevel

from ego.gitlab_core.auth.Auth import Auth


class GitlabClient(Auth):
    def __init__(self, url, token, **kwargs):
        super(GitlabClient, self).__init__(url, token, **kwargs)

    def search_projects(self, keyword, page_no=1, page_size=10):
        """
            全局项目搜索
            keyword：项目元数据关键字
            page_no: 页码
            page_size：每页行数
        """
        return self.gl_inst.search(SearchScope.PROJECTS, keyword, page=page_no, per_page=page_size)

    def query_projects_by_group_id(self, group_id, **kwargs):
        """
            使用group_id获取项目列表
        """
        group = self.gl_inst.groups.get(group_id)
        return group.projects.list(**kwargs)

    def query_projects(self, **kwargs):
        """
            search: 返回符合搜索条件的项目列表（一般输入项目名关键字）
            membership：是否受项目成员限制，默认：True,
            archived：是否受归档状态限制，默认：True,
            owned：是否受项目归属限制，默认：True,
            min_access_level：指定项目针对当前用户的最低访问级别
                    Guest -> 10; Reporter -> 20; Developer -> 30; Maintainer -> 40; Owner -> 50
            page: 页码
            per_page：每页行数
            order_by：指定排序字段（id、name、path、created_at、updated_at、last_activity_at、similarity）
            iterator：查询所有，并使用生成器返回，默认False
            all：查询所有，默认False
        """
        return self.gl_inst.projects.list(**kwargs)

    def query_project_by_project_id(self, project_id):
        """
            通过仓库ID获取项目信息
        """
        return self.gl_inst.projects.get(project_id)

    def query_project_commits(self, project_id, **kwargs):
        """
            获取仓库commit列表
            page: 页码
            per_page：每页行数
            ref_name：[branch_name | tag]
            since: start_time
            until: end_time
            iterator：查询所有，默认False
            all：查询所有，默认False
        """
        return self.gl_inst.projects.get(project_id).commits.list(**kwargs)

    def query_project_branches(self, project_id, b_keyword=None, page=1, per_page=10):
        """
            通过仓库ID获取分支列表
        """
        project = self.query_project_by_project_id(project_id=project_id)
        return project.branches.list(id=project_id, search=b_keyword, page=page, per_page=per_page)

    def query_project_tags(self, project_id, t_keyword=None, page=1, per_page=10):
        """
            通过仓库ID获取TAG列表
        """
        project = self.query_project_by_project_id(project_id=project_id)
        return project.tags.list(search=t_keyword, page=page, per_page=per_page)

    def download_repository_archive(self, project_id, repo_ref, target_path, **kwargs):
        """
            拉取指定分支/TAG/Commit对应的存储库内容
        """
        project = self.query_project_by_project_id(project_id=project_id)
        project_package = project.repository_archive(sha=repo_ref, **kwargs)
        with open(target_path, "wb+") as file:
            file.write(project_package)

    def query_project_hooks(self, project_id):
        """
            获取指定项目的webhooks
        """
        project = self.query_project_by_project_id(project_id=project_id)
        hooks = project.hooks.list()
        return hooks

    def query_project_hook_by_id(self, project_id, hook_id):
        """
            获取指定项目的webhooks
        """
        project = self.query_project_by_project_id(project_id=project_id)
        hook = project.hooks.get(id=hook_id)
        return hook

    def create_project(self, project_name, **kwargs):
        """
            创建项目
            project_name: 项目名（必填）
            username: 归属用户
            namespace_id: 项目组ID/工作空间ID
            default_branch: 默认分支
            description: 项目描述
        """
        if "username" in kwargs and kwargs["username"]:
            return self.create_project_by_user(project_name=project_name, **kwargs)

        create_params = {"name": project_name}
        create_params.update(kwargs)
        project = self.gl_inst.projects.create(create_params)
        return project

    def create_project_by_user(self, username, project_name, **kwargs):
        """
            为指定用户创建项目
            username: 归属用户（必填）
            project_name: 项目名（必填）
            namespace_id: 项目组ID/工作空间ID
            default_branch: 默认分支
            description: 项目描述
        """
        user = self.gl_inst.users.list(username=username)[0]
        create_params = {"name": project_name}
        create_params.update(kwargs)
        user_project = user.projects.create(create_params)
        return user_project

    def add_project_member(self, project_id, username, access_level=None):
        """
            为指定项目添加成员
            project_id: 项目ID
            username: 归属用户（必填）
            access_level: 访问级别  from gitlab.const import AccessLevel
        """
        user = self.gl_inst.users.list(username=username)[0]
        project = self.query_project_by_project_id(project_id=project_id)
        member_object = project.members.create({
            "user_id": user.id,
            "access_level": access_level if access_level else AccessLevel.MINIMAL_ACCESS
        })
        return member_object

    def update_project_member(self, project_id, username, access_level=None):
        """
            更新指定项目成员
            project_id: 项目ID
            username: 归属用户（必填）
            access_level: 访问级别  from gitlab.const import AccessLevel
        """
        user = self.gl_inst.users.list(username=username)[0]
        project = self.query_project_by_project_id(project_id=project_id)
        member = project.members.get(user.id)
        member.access_level = access_level if access_level else AccessLevel.MINIMAL_ACCESS
        member.save()
        return member

    def delete_project_member(self, project_id, username):
        """
            删除指定项目成员
            project_id: 项目ID
            username: 归属用户（必填）
        """
        user = self.gl_inst.users.list(username=username)[0]
        project = self.query_project_by_project_id(project_id=project_id)
        project.members.delete(user.id)
