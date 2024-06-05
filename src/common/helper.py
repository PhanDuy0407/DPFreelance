from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from config import CONF
from persistent.AccountPersistent import AccountPersistent
from persistent.RecruiterPersistent import RecruiterPersistent
from persistent.ApplicantPersistent import ApplicantPersistent
from common.database_connection import get_db
from common.constant import RECRUITER_ROLE, ADMIN_ROLE, APPLICANT_ROLE
from models.dto.output.AccountDTO import Account, ApplicantDTO, RecruiterInfoDTO
from models.dto.output.UserInformation import UserInformation

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def get_current_user(role = ["*"]):
    def role_checker(token: str = Depends(oauth2_scheme), session = Depends(get_db)):
        auth_config = CONF["Auth"]
        persistent = AccountPersistent(session)
        recruiter_persistent = RecruiterPersistent(session)
        applicant_persistent = ApplicantPersistent(session)
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
        forbidden_exception = HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Resource forbidden",
        )
        try:
            payload = jwt.decode(token, auth_config.get("secret_key"), algorithms=[auth_config.get("algorithm")])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
        except jwt.ExpiredSignatureError:
            raise credentials_exception
        except jwt.DecodeError:
            raise credentials_exception
        user = persistent.get_account_by_username(username)
        if user is None:
            raise credentials_exception

        applicant = applicant_persistent.get_applicant_by_account_id(user.id)
        recruiter = recruiter_persistent.get_recruiter_by_account_id(user.id)
        user_dict = user.to_dict()
        user = Account(
            **user_dict,
            applicant=ApplicantDTO(**applicant.to_dict(), information=UserInformation(**user_dict)) if applicant else None,
            recruiter=RecruiterInfoDTO(**recruiter.to_dict(), information=UserInformation(**user_dict)) if recruiter else None
        )
        if "*" in role:
            return user
        elif ADMIN_ROLE in role and user.is_admin:
            return user
        else:
            if APPLICANT_ROLE in role and user.applicant:
                return user
            if RECRUITER_ROLE in role and user.recruiter:
                return user

        raise forbidden_exception

    return role_checker

def get_filters(params, Model):
    filters = []
    operators = {
        'eq': '=',
        'gt': '>',
        'lt': '<',
        'ge': '>=',
        'le': '<='
    }
    
    # Dynamically add filters based on query parameters
    for key, value in params.items():
        if '__' in key:
            field_name, op = key.split('__')
            if field_name in Model.filter_fields() and op in operators:
                column = getattr(Model, field_name)
                if op == 'eq':
                    filters.append(column == value)
                elif op == 'gt':
                    filters.append(column > value)
                elif op == 'lt':
                    filters.append(column < value)
                elif op == 'ge':
                    filters.append(column >= value)
                elif op == 'le':
                    filters.append(column <= value)
            else:
                raise HTTPException(status_code=400, detail=f"Invalid filter key: {key}")
    return filters

def parse_order_by(params, Model):
    order_criteria = []
    if params.get("order_by"):
        for order in params.get("order_by", "").split(","):
            print(order)
            key, direction = order.split(":")
            if key in Model.order_by_fields():
                if direction not in ["asc", "desc"]:
                    raise HTTPException(status_code=400, detail=f"Invalid sort direction: {direction}")
                order_criteria.append((key, direction))
            else:
                raise HTTPException(status_code=400, detail=f"Invalid order key: {key}")
    return order_criteria
