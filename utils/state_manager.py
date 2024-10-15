from models import db, UserState

class StateManager:
    def get_state(self, user_phone):
        user_state = UserState.query.filter_by(user_phone=user_phone).first()
        if user_state:
            return user_state.state_data
        return None

    def set_state(self, user_phone, state_data):
        user_state = UserState.query.filter_by(user_phone=user_phone).first()
        if not user_state:
            user_state = UserState(user_phone=user_phone, state_data=state_data)
            db.session.add(user_state)
        else:
            user_state.state_data = state_data
        db.session.commit()

    def update_state(self, user_phone, state_update):
        user_state = UserState.query.filter_by(user_phone=user_phone).first()
        if user_state:
            user_state.state_data.update(state_update)
            db.session.commit()

    def clear_state(self, user_phone):
        user_state = UserState.query.filter_by(user_phone=user_phone).first()
        if user_state:
            db.session.delete(user_state)
            db.session.commit()
