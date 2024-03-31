import helper

orig_df = helper.read_data()

df = helper.clean_data(orig_df.copy())

_map = helper.create_mapping(orig_df.copy())

df = helper.resample_data(orig_df.copy(), _map)
