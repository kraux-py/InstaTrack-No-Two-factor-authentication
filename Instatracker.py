import instaloader

def login(username, password):
    try:
        L = instaloader.Instaloader()
        L.context.log("Logging in...")
        L.login(username, password)
        L.context.log("Login successful!")
        return L
    except instaloader.exceptions.TwoFactorAuthRequiredException:
        two_factor_code = input("Enter the two-factor authentication code: ")
        L.context.two_factor_code = two_factor_code
        L.context.log("Two-factor authentication code entered")
        L.context.log("Logging in...")
        L.login(username, password)
        L.context.log("Login successful!")
        return L
    except instaloader.exceptions.InvalidArgumentException as e:
        print("Login failed:", e)
    except instaloader.exceptions.BadCredentialsException as e:
        print("Login failed: Incorrect password.")
    except Exception as e:
        print("An unexpected error occurred during login:", e)
    return None

def get_followers_and_following(L, username):
    try:
        profile = instaloader.Profile.from_username(L.context, username)
        followers = profile.get_followers()
        following = profile.get_followees()

        followers_list = [f"{follower.username} - https://www.instagram.com/{follower.username}/" for follower in followers]
        following_list = [f"{user.username} - https://www.instagram.com/{user.username}/" for user in following]

        unfollowers = set(following_list) - set(followers_list)
        not_following_back = set(followers_list) - set(following_list)

        print("Followers:")
        for follower in followers_list:
            print(follower)

        print("\nFollowing:")
        for user in following_list:
            print(user)

        print(f"\nTotal followers: {len(followers_list)}")
        print(f"Total following: {len(following_list)}")
        print(f"Total not following back: {len(not_following_back)}")

        print("\nUsers who don't follow you back:")
        for user in unfollowers:
            print(user)

    except Exception as e:
        print("An unexpected error occurred while getting followers:", e)

def main():
    username = input("Enter your Instagram username: ")
    password = input("Enter your Instagram password: ")

    while True:
        L = login(username, password)
        if L:
            get_followers_and_following(L, username)
            break
        else:
            password = input("Enter your Instagram password again: ")

if __name__ == "__main__":
    main()
