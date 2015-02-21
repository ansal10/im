from datetime import datetime
import pdb
from django.contrib.auth.models import User
from django.db import transaction
from hw.homework.helper import validateDateTime
from hw.models import Project, Bid, Profile


def applyBid(user_id=None, project_id=None, bidform=None):
    if user_id and project_id and bidform:
        try:
            user = User.objects.get(id=user_id)
            project = Project.objects.get(id=project_id)
            if bidform.is_valid():
                formdata = bidform.cleaned_data
                print "formdata  = ",formdata
            else:
                return ["Error occur while saving the BID, Please Retry"]

            description = formdata['description']
            status='ACTIVE'
            amount=formdata['amount']
            deliever_by,flag = validateDateTime(formdata['deliver_by'])
            deleteable = formdata['deletable']
            if flag is False:
                return [deliever_by]

            if deleteable:
                Bid.objects.filter(user=user, project=project).update( deleted_on=datetime.now(), status='DEL')
                return ["Sucessfully deleted the bid"]
            else:
                if Bid.objects.filter(user=user, project=project).__len__()==0:
                    bid=Bid(user=user, project=project, description=description, status=status, amount=amount, deliever_by=deliever_by)
                    bid.save()
                    return []

                elif Bid.objects.filter(user=user, project=project).__len__()==1:
                    Bid.objects.filter(user=user, project=project).update(description=description, deliever_by=deliever_by, status=status, amount=amount, deleted_on=None)
                    return []

        except Exception, e:
            print e
            return ["Error occur while saving the BID, Please Retry"]


def getBids(user_id=None):
    if user_id is None:
        return ["Some Error Occured , please goto Dashboard"],None
    else:
        bids = Bid.objects.filter(user_id=user_id)
        return [],bids


def confirmBid(user_id=None, project_id=None, bid_id=None):
    try:
        project=Project.objects.get(id=project_id, deleted_on=None)
        bid=Bid.objects.get(id=bid_id, deleted_on=None)
        if project.assigned_to:
            return ["Your Project is already assigned to %s"%(project.alloted_to.username)],[]
        if project.user.id==int(user_id) and bid.project.id==int(project_id):
            if project.user.profile.balance>=bid.amount:
                with transaction.commit_on_success:
                    # 1. update Project alloted
                    # 2. update students amount
                    # 3. delete bids of all other User
                    # 4. update users bid to Wins
                    now = datetime.now()
                    Project.objects.filter(id=project_id, deleted_on=None).update(assigned_to_id=user_id, assigned_on=now, status='PROG')
                    Profile.objects.filter(user_id=user_id, deleted_on=None).update(balance=(project.user.balance-bid.amount))
                    Bid.objects.filter(project=project).update(deleted_on=now, status='DENY')
                    Bid.objects.filter(project=project, user_id=user_id).update(status='WINS', deleted_on=None)

                return [],["Your Project had been Successfully Assigned to %s" %(project.user.username)]
            else:
                return ["You do not have Sufficient balance to select this bid"],["You can try for other bids or add money to your account"]
        else:
            return ["Some Error occured, the project and bids do not seems to be related"],[]
    except Exception, e:
        print e
        return ["Some error occured while confirming your bid , please try again"],[]


def deleteBids(project_id=None):
    project = Project.objects.get(id=project_id)
    bidder=project.assigned_to
    student=project.user
    bid=Bid.objects.get(status='WIN', project_id=project_id, user=bidder )

    with transaction.commit_on_success:
        Project.objects.filter(id=project_id).update(assigned_to_id=None, assigned_on=None, status='LIVE')
        profile = Profile.objects.get(user=student)
        profile.balance = profile.balance-bid.amount
        profile.save()
        Bid.objects.filter(project_id=project_id, status__in=['DENY','WINS']).update(deleted_on=None, status='ACTIVE')

