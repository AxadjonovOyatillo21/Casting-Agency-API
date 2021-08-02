from flask import abort

# {{ Validators }}


DATA_PER_PAGE = 10


class DataBaseError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def paginate_data(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * DATA_PER_PAGE
    end = start + DATA_PER_PAGE
    current_data = selection[start:end]

    return current_data


def check_actor(actor, actor_id):
    if not actor:
        raise DataBaseError({
            "message": "Actor with id {} not found".format(actor_id)
        }, 404)


def check_movie(movie, movie_id):
    if not movie:
        raise DataBaseError({
            "message": "Movie with id {} not found".format(movie_id)
        }, 404)


def check_genre(genre, genre_id):
    if not genre:
        raise DataBaseError({
            "message": "Genre with id {} not found".format(genre_id)
        }, 404)


def string_validator(data):
    if data:
        if isinstance(data, str) and len(data) >= 3:
            return True
        else:
            abort(400)
    return False


def id_validator(data):
    if data:
        if isinstance(data, list) and len(data) > 0:
            for data_id in data:
                data_id = str(data_id)
                if (data_id.isdigit() and int(data_id) >= 0) == False:
                    abort(400)
            return True
        else:
            abort(400)
    else:
        return False


def age_validator(age):
    if age:
        try:
            age = int(age)
            return True
        except ValueError:
            abort(400)
    return False


def man_or_woman(gender):
    genders = ["man", "woman"]
    if gender:
        if isinstance(gender, str):
            if gender in genders:
                return True
            else:
                abort(400)
    return False


def date_validator(data):
    if data:
        if isinstance(data, str):
            if "/" in data:
                data = data.split('/')
                if len(data) != 3:
                    abort(400)
                else:
                    for date in data:
                        date = str(date)
                        if date.isdigit() == False:
                            abort(400)
                    if int(data[0]) > 31 or int(data[0]) <= 0:
                        abort(400)
                    if int(data[1]) > 12 or int(data[1]) <= 0:
                        abort(400)
                    return True
            else:
                abort(400)
        else:
            abort(400)
    else:
        return False
