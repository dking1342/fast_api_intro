-- counting user blogs
SELECT users.user_id, users.email, COUNT(blogs.user_id) AS user_blog_count
FROM blogs
RIGHT JOIN users ON blogs.user_id = users.user_id
GROUP BY users.user_id;

--joining blogs and users table
SELECT blogs.*, users.email
FROM blogs
LEFT JOIN users ON blogs.user_id = users.user_id;

--joining blogs and votes looking at the blogs
SELECT *
FROM blogs
LEFT JOIN votes ON blogs.blog_id = votes.blog_id;

-- counting blogs with votes
SELECT blogs.*, COUNT(votes.blog_id) AS likes
FROM blogs
LEFT JOIN votes ON blogs.blog_id = votes.blog_id
GROUP BY blogs.blog_id;

-- get blog by id and find the number of votes
SELECT blogs.*, COUNT(votes.blog_id) AS likes
FROM blogs
LEFT JOIN votes ON blogs.blog_id = votes.blog_id
WHERE blogs.blog_id = 'dc6aeb36-4094-4c6e-9db6-9cb0cf1ab6d9'
GROUP BY blogs.blog_id;
