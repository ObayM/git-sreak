import os
from supabase import create_client, Client

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)


def add_new_user(github_handle, slack_user_id):
    try:
        supabase.table('users').insert({
            'github_handle': github_handle,
            'slack_user_id': slack_user_id
        }).execute()

        print(f"New person joined the challenge : {github_handle}")
    except Exception as e:
        print(f"error adding new user {github_handle}: {e}")

def get_active_users():
    try:
        response = supabase.table('users').select('*').eq('is_active', True).execute()

        return response.data
    
    except Exception as e:
        print(f"erorr fetching the data: {e}")
        return []

def update_user_streak(github_handle, new_streak, last_commit_date):

    try:
        supabase.table('users').update({
            'current_streak': new_streak,
            'last_commit_date': last_commit_date
        }).eq('github_handle', github_handle).execute()

        print(f"updated the streak for {github_handle} to {new_streak}")

    except Exception as e:
        print(f"erorr updating streak for {github_handle}: {e}")


def reset_user_streak(github_handle):
    try:
        supabase.table('users').update({'current_streak': 0}).eq('github_handle', github_handle).execute()

        print(f"Streak broken for: {github_handle}")
    except Exception as e:
        print(f"error happend for {github_handle}: {e}")