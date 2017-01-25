from django.shortcuts import render, redirect, get_object_or_404
from portfolio_manager.models import *
from portfolio_manager.forms import *
from django.contrib.contenttypes.models import ContentType
import logging

# LOGGING
logger = logging.getLogger('django.request')

# Site to see history of projects
def history(request):
    history_all = Project.history.all()
    names = {}
    orgs = {}
    dates = {}
    for h in history_all:
        names[h.id] = []
        orgs[h.id] = []
        dates[h.id] = []
    for h in history_all:
        names[h.id].append(h.name)
        orgs[h.id].append(h.parent)
        dates[h.id].append(h.history_date)

    return render(request, 'history.html', {'ids':range(1, len(names)+1), 'names':names, 'orgs':orgs, 'dates':dates})

# Site to upload a new project
def add_new_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            # Save a new Organization
            organization = Organization(name = form.cleaned_data['organization'])
            organization.save()

            # Save a new Project
            newproject = Project(name = form.cleaned_data['name'], parent = organization)
            newproject.save()

            # Make ProjectDimension for owner
            project_dimension_owner = ProjectDimension(dimension_object=newproject, project=newproject)
            project_dimension_owner.save()

            # Make AssociatedPersonDimension
            pers = get_object_or_404(Person, pk=form.cleaned_data['owner'].pk)
            assPerson = AssociatedPersonDimension(value=pers, name=str(pers))
            assPerson.save()

            # Make ProjectOwnerDimension
            own = ProjectOwnerDimension(assPerson=assPerson)
            own.save()

           # Link owner to project
            project_dimension_owner.dimension_object=own
            project_dimension_owner.save()

            #######################
            ####    BUDGET  #######
            #######################

            #Project Dimension for budget
            project_dimension_budget = ProjectDimension(dimension_object=newproject, project=newproject)
            project_dimension_budget.save()

            # Make budjet dimension
            budget = DecimalDimension(name="budget", value=form.cleaned_data['budget'])
            budget.save()

            # Link budget to project
            project_dimension_budget.dimension_object=budget
            project_dimension_budget.save()

            form = ProjectForm()
        return redirect('projects')

    elif request.method == 'GET':
        form = ProjectForm()
    return render(request, 'uploadproject.html', {'form': form})

# Site to add a new organization
def add_new_org(request):
    if request.method == 'POST':
        form = OrganizationForm(request.POST)
        if form.is_valid():
            organization = Organization(name = form.cleaned_data['name'])
            organization.save()
        return redirect('add_new_project')

    elif request.method == 'GET':
        form = OrganizationForm()
    return render(request, 'new_org.html', {'form':form})

# Site to add a new person
def add_new_person(request):
    if request.method == 'POST':
        form = PersonForm(request.POST)
        if form.is_valid():
            person = Person(first_name=form.cleaned_data['first'], last_name=form.cleaned_data['last'])
            person.save()
        return redirect('add_new_project')

    elif request.method == 'GET':
        form = PersonForm()
    return render(request, 'new_person.html', {'form':form})

# Site to see all projects
def projects(request):
    projects_all = Project.objects.all()
    return render(request, 'projects.html', {'projects': projects_all})

# Site to see all organizations
def organizations(request):
   if request.method == "POST":
      form = CronForm(request.POST)

      if form.is_valid:
         projs = Project.objects.filter(parent=request.POST.get("orgs", ""))

         #redirect to the url where you'll process the input
         return render(request, 'projects_by_organization.html', {'projs':projs}) # insert reverse or url
   else:
        form = CronForm()
   return render(request, 'droptable_organization.html', {'form':form})


def show_project(request, project_id):
        theProject = get_object_or_404(Project, pk=project_id)
        pod = ContentType.objects.get_for_model(ProjectOwnerDimension)
        dd = ContentType.objects.get_for_model(DecimalDimension)
        owner = ProjectDimension.objects.filter(content_type=pod, project_id=theProject.id).first().dimension_object.assPerson.value   # ONLY WORKS IF THERE IS ONLY ONE OWNER
        budget = ProjectDimension.objects.filter(content_type=dd, project_id=theProject.id).first().dimension_object.value
        extraFields = InsertedField.objects.filter(parent=theProject)


        return render(request, 'project.html', {'project': theProject, 'extraField': extraFields, 'owner': owner, 'budget':budget })

def project_edit(request, project_id):
    proj = get_object_or_404(Project, pk=project_id)
    if request.method == "POST":
        form = ProjectForm(request.POST)

        if form.is_valid():
            # Update the projects info
            proj.name = form.cleaned_data['name']
            proj.parent = form.cleaned_data['parent']
            proj.save()

        return redirect('show_project', project_id=proj.pk)
    else:
        data = {
    'name': proj.name,
    'parent': proj.parent
}
        form = ProjectForm(data)
    return render(request, 'project_edit.html', {'form': form})


def insert_field(request, project_id):
    proj = get_object_or_404(Project, pk=project_id)
    if request.method == 'POST':
        form = TableSpecification(request.POST)
        if form.is_valid():
            if form.cleaned_data['datatype']=='TXT':
                insField = InsertedField(name = form.cleaned_data['name'], parent=proj, textValue=form.cleaned_data['value'])
                insField.save()
                return redirect('show_project', project_id=proj.pk)
            else:
                insField = InsertedField(name = form.cleaned_data['name'], parent=proj, numericalValue=float('0' + form.cleaned_data['value']))
                insField.save()
                return redirect('show_project', project_id=proj.pk)
        else:
            formt = TableSpecification()
            return render(request, 'insert_field.html', {'formt':formt})
    elif request.method == 'GET':
        data = {
            'name': proj.name,
            'parent': proj.parent,
            'unit': proj.name,
        }
        formt = TableSpecification()
        return render(request, 'insert_field.html', {'formt':formt})
