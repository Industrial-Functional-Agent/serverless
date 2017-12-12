from models import Post


if not Post.exists():
    Post.create_table(read_capacity_units=5, write_capacity_units=5)
    print('Post table has been created.')
