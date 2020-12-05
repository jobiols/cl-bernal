            SELECT
                sq.survey_id,
                sq.id+sl.id as id,
                sq.title as question,
                sl.value as answer,
                count(sl.value) as participation,
                count(*) as participationx100
            FROM survey_question sq
            JOIN survey_user_input_line suil
            ON sq.id = suil.question_id
            JOIN survey_label sl
            ON sl.id = suil.value_suggested
        where sq.question_type = 'simple_choice'
        group by sl.value, sq.title, sq.id, sl.id
        order by sq.title
