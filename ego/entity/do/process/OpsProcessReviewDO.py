from sqlalchemy import Column
from sqlalchemy import SmallInteger, BigInteger, String, DateTime

from ego.entity.base.BaseEntity import Base, BaseEntity


class OpsProcessReviewDO(Base, BaseEntity):
    __tablename__ = "ops_process_review"

    review_id = Column(BigInteger, primary_key=True, autoincrement=True)
    process_id = Column(BigInteger)
    process_no = Column(String(64))
    step_id = Column(String(64))
    step_name = Column(String(128))
    reviewer = Column(String(64))
    reviewer_id = Column(BigInteger)
    opinion = Column(SmallInteger)
    reason = Column(String(255))
    create_time = Column(DateTime)
    update_time = Column(DateTime)
