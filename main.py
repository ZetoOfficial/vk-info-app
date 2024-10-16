from argument_parser import parse_arguments
from config import DEFAULT_ENV_FILE
from env_loader import load_environment
from utils import save_to_json
from vk_api import fetch_vk_data, get_access_token, get_current_user_id


def main():
    args = parse_arguments()
    load_environment(DEFAULT_ENV_FILE)

    token = get_access_token()

    user_id = args.user_id
    if user_id.lower() == "self":
        user_id = get_current_user_id(token)

    data = fetch_vk_data(user_id, token)
    save_to_json(data, args.output)
    print(f"Data successfully saved to {args.output}")


if __name__ == "__main__":
    main()
