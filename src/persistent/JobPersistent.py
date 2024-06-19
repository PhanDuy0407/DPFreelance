from uuid import uuid4
from sqlalchemy.orm import aliased
from models.data.Job import Job
from models.data.JobApply import JobApply
from models.data.Category import Category
from models.data.Recruiter import Recruiter
from models.data.Applicant import Applicant
from models.data.Account import Account
from sqlalchemy.orm.session import Session
from sqlalchemy import and_
from sqlalchemy import func
from common.helper import get_filters, parse_order_by
from common.constant import JobStatus, JobApplyStatus
from persistent.BasePersistent import BasePersistent

class JobPersistent(BasePersistent):
    
    def get_all_jobs(self, params):
        query = self.session.query(
            Job,
            Category,
            Recruiter,
            Account,
            func.count(JobApply.applicant_id).label("number_of_applied")
        ).filter(
            Category.id == Job.category_id,
            Recruiter.id == Job.poster_id,
            Account.id == Recruiter.account_id,
        ).outerjoin(
            JobApply, JobApply.job_id == Job.id
        ).group_by(Job.id)
        filters = get_filters(params, Job)
        if filters:
            query = query.filter(and_(*filters))
        order_criteria = parse_order_by(params, Job)
        for key, direction in order_criteria:
            column = getattr(Job, key)
            if direction == "asc":
                query = query.order_by(column.asc())
            else:
                query = query.order_by(column.desc())
        return query.limit(params.get("limit")).offset(params.get("offset")).all()
    
    def get_job_by_id(self, job_id):
        return self.session.query(
            Job,
            Category,
            Recruiter,
            Account,
            func.count(JobApply.applicant_id).label("number_of_applied")
        ).filter(
            Job.id == job_id,
            Category.id == Job.category_id,
            Recruiter.id == Job.poster_id,
            Account.id == Recruiter.account_id
        ).outerjoin(
            JobApply, JobApply.job_id == Job.id
        ).group_by(Job.id).first()
    
    def get_job_applied_by_applicant_id(self, applicant_id, params):
        subq = self.session.query(
            JobApply.job_id,
            func.count(JobApply.applicant_id).label('number_of_applied')
        ).group_by(JobApply.job_id).subquery()

        query = self.session.query(
            JobApply,
            Job,
            Category,
            Recruiter,
            Account,
            subq.c.number_of_applied
        ).filter(
            JobApply.applicant_id == applicant_id,
            Job.id == JobApply.job_id,
            Category.id == Job.category_id,
            Recruiter.id == Job.poster_id,
            Account.id == Recruiter.account_id
        ).join(subq, Job.id == subq.c.job_id)

        filters = get_filters(params, JobApply)
        if filters:
            query = query.filter(and_(*filters))
        return query.order_by(JobApply.created_at.desc()).all()
    
    def add_job(self, job):
        self.session.add(job)
        self.session.commit()
        return job
    
    def edit_job(self, job_id, job):
        self.session.query(Job).filter(
            Job.id == job_id
        ).update(job, synchronize_session=False)
        self.session.commit()
    
    def add_job_apply(self, job_apply):
        self.session.add(job_apply)
        self.session.commit()
        return job_apply
    
    def get_jobs_apply_by_job_id(self, job_id):
        return self.session.query(JobApply, Applicant, Account).filter(
            JobApply.job_id == job_id,
            Applicant.id == JobApply.applicant_id,
            Account.id == Applicant.account_id,
        ).all()
    
    def get_job_apply_by_job_id_and_applicant_id(self, job_id, applicant_id):
        return self.session.query(
            JobApply,
            Job,
            Recruiter,
        ).filter(
            JobApply.applicant_id == applicant_id,
            JobApply.job_id == job_id,
            Job.id == JobApply.job_id,
            Recruiter.id == Job.poster_id,
        ).first()
    
    def get_all_jobs_by_recruiter_id(self, recruiter_id, params):
        query = self.session.query(
            Job,
            Category,
            func.count(JobApply.applicant_id).label("number_of_applied")
        ).filter(
            Category.id == Job.category_id,
            Job.poster_id == recruiter_id
        ).outerjoin(
            JobApply, JobApply.job_id == Job.id
        ).group_by(Job.id)
        filters = get_filters(params, Job)
        if filters:
            query = query.filter(and_(*filters))
        return query.order_by(Job.created_at.desc()).all()
    
    def deny_all_waiting_job_apply(self, job_id):
        query = self.session.query(JobApply).filter(
            JobApply.job_id == job_id,
            JobApply.status == JobApplyStatus.WAITING_FOR_APPROVE,
        )
        list_job_deny = query.all()
        query.update({"status": JobStatus.DENY})
        return list_job_deny

    def get_job_applied_success_by_job_id(self, job_id, apply_status):
        query = self.session.query(JobApply, Applicant, Account).filter(
            JobApply.job_id == job_id,
            Applicant.id == JobApply.applicant_id,
            Account.id == Applicant.account_id,
        )
        if apply_status:
            query = query.filter(JobApply.status == apply_status)
        else:
            query = query.filter(JobApply.status.in_([JobApplyStatus.ACCEPTED, JobStatus.DONE]))
        return query.first()

    
    def delete_job(self, job):
        self.session.delete(job)
        self.commit_change()

    def get_all_job_applies_success(self, params):
        subq = self.session.query(
            JobApply.job_id,
            func.count(JobApply.applicant_id).label('number_of_applied')
        ).group_by(JobApply.job_id).subquery()

        query = self.session.query(
            JobApply,
            Job,
            Category,
            subq.c.number_of_applied
        ).filter(
            JobApply.status.in_([JobApplyStatus.ACCEPTED, JobApplyStatus.DONE]),
            Job.id == JobApply.job_id,
            Category.id == Job.category_id,
        ).join(subq, Job.id == subq.c.job_id)

        filters = get_filters(params, JobApply)
        if filters:
            query = query.filter(and_(*filters))

        job_applies = query.order_by(JobApply.created_at.desc()).all()
        result = []
        for job_apply, job, category, number_of_applied in job_applies:
            poster, poster_account = self.session.query(
                Recruiter,
                Account
            ).filter(
                Recruiter.id == Job.poster_id,
                Job.id == job_apply.job_id,
                Account.id == Recruiter.account_id
            ).first()

            applicant, applicant_account = self.session.query(
                Applicant,
                Account
            ).filter(
                Applicant.id == job_apply.applicant_id,
                Account.id == Applicant.account_id
            ).first()
            result.append((job_apply, job, category, applicant, applicant_account, poster, poster_account, number_of_applied))
        return result


    # def get_all_job_applies_success(self, params):
    #     subq = self.session.query(
    #         JobApply.job_id,
    #         func.count(JobApply.applicant_id).label('number_of_applied')
    #     ).group_by(JobApply.job_id).subquery()

    #     # Aliases for Recruiter and Account
    #     RecruiterAlias = aliased(Recruiter, name="recruiter_alias")
    #     AccountAlias = aliased(Account, name="account_alias")

    #     # Subquery for getting job and recruiter details
    #     subq_recruiter = self.session.query(
    #         Job.id.label("job_id"),
    #         RecruiterAlias.id.label("recruiter_id"),
    #         AccountAlias.id.label("account_id"),
    #     ).filter(
    #         Job.poster_id == RecruiterAlias.id,
    #         AccountAlias.id == RecruiterAlias.account_id,
    #     ).subquery()

    #     # Main query
    #     query = self.session.query(
    #         JobApply,
    #         Job,
    #         Category,
    #         Applicant,
    #         Account,
    #         RecruiterAlias,
    #         AccountAlias,
    #         subq.c.number_of_applied
    #     ).filter(
    #         JobApply.status.in_([JobApplyStatus.ACCEPTED, JobApplyStatus.DONE]),
    #         Job.id == JobApply.job_id,
    #         Category.id == Job.category_id,
    #         Applicant.id == JobApply.applicant_id,
    #         Account.id == Applicant.account_id
    #     ).join(subq, Job.id == subq.c.job_id).join(
    #         subq_recruiter, Job.id == subq_recruiter.c.job_id
    #     ).join(
    #         RecruiterAlias, RecruiterAlias.id == subq_recruiter.c.recruiter_id
    #     ).join(
    #         AccountAlias, AccountAlias.id == subq_recruiter.c.account_id
    #     )

    #     # Apply additional filters if any
    #     filters = get_filters(params, JobApply)
    #     if filters:
    #         query = query.filter(and_(*filters))

    #     # Execute the query and return results
    #     return query.order_by(JobApply.created_at.desc()).all()