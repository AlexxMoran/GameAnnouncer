from models.base import Base


def test_base_columns_and_repr():
    class D(Base):
        __tablename__ = "dummies"

    cols = D.__table__.columns
    assert "id" in cols
    assert "created_at" in cols
    assert "updated_at" in cols

    d = D()
    d.id = 1
    assert repr(d) == "<D(id=1)>"
