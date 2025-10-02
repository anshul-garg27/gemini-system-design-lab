#!/usr/bin/env python3
"""
Simple API Key Health Checker
Checks all API keys without sending prompts - just tests the API endpoint directly
"""
import requests
import json
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

class SimpleAPIKeyChecker:
    def __init__(self):
        self.api_keys = []
        self.load_api_keys()
    
    def load_api_keys(self):
        """Load API keys from config.py"""
        try:
            # Add current directory to path
            sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
            from config import API_KEYS
            if API_KEYS and len(API_KEYS) > 0:
                self.api_keys = API_KEYS.copy()
                print(f"✅ Loaded {len(self.api_keys)} API keys from config.py")
            else:
                print("❌ No API keys found in config.py")
                sys.exit(1)
        except ImportError as e:
            print(f"❌ Error loading config.py: {e}")
            sys.exit(1)
    
    def test_api_key(self, key_index, api_key):
        """Test a single API key with a minimal request"""
        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
        
        headers = {
            "Content-Type": "application/json",
            "X-goog-api-key": api_key
        }
        
        # Minimal payload - just ask for "test" without sending complex prompt
        payload = {
            "contents": [{
                "parts": [{
                    "text": "test"
                }]
            }]
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=10)
            
            if response.status_code == 200:
                return {
                    "index": key_index,
                    "key": api_key[:10] + "...",
                    "status": "WORKING",
                    "error": None,
                    "status_code": response.status_code
                }
            elif response.status_code == 429:
                return {
                    "index": key_index,
                    "key": api_key[:10] + "...",
                    "status": "RATE_LIMITED",
                    "error": "Too many requests",
                    "status_code": response.status_code
                }
            elif response.status_code == 403:
                try:
                    error_data = response.json()
                    error_msg = error_data.get('error', {}).get('message', 'Unknown error')
                    if 'quota' in error_msg.lower():
                        status = "QUOTA_EXCEEDED"
                    else:
                        status = "INVALID_KEY"
                    return {
                        "index": key_index,
                        "key": api_key[:10] + "...",
                        "status": status,
                        "error": error_msg,
                        "status_code": response.status_code
                    }
                except:
                    return {
                        "index": key_index,
                        "key": api_key[:10] + "...",
                        "status": "INVALID_KEY",
                        "error": "Invalid API key",
                        "status_code": response.status_code
                    }
            elif response.status_code == 401:
                return {
                    "index": key_index,
                    "key": api_key[:10] + "...",
                    "status": "INVALID_KEY",
                    "error": "Unauthorized - Invalid API key",
                    "status_code": response.status_code
                }
            else:
                return {
                    "index": key_index,
                    "key": api_key[:10] + "...",
                    "status": "ERROR",
                    "error": f"HTTP {response.status_code}: {response.text[:100]}",
                    "status_code": response.status_code
                }
                
        except requests.exceptions.Timeout:
            return {
                "index": key_index,
                "key": api_key[:10] + "...",
                "status": "TIMEOUT",
                "error": "Request timeout",
                "status_code": None
            }
        except requests.exceptions.ConnectionError:
            return {
                "index": key_index,
                "key": api_key[:10] + "...",
                "status": "CONNECTION_ERROR",
                "error": "Connection failed",
                "status_code": None
            }
        except Exception as e:
            return {
                "index": key_index,
                "key": api_key[:10] + "...",
                "status": "ERROR",
                "error": str(e),
                "status_code": None
            }
    
    def check_all_keys(self):
        """Check all API keys concurrently"""
        print(f"\n🔍 Checking {len(self.api_keys)} API keys...")
        print("-" * 80)
        
        results = []
        
        # Check all keys concurrently (max 10 threads to avoid rate limiting)
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = []
            
            for i, api_key in enumerate(self.api_keys):
                future = executor.submit(self.test_api_key, i, api_key)
                futures.append(future)
            
            # Process results as they complete
            for future in as_completed(futures):
                result = future.result()
                results.append(result)
                
                # Show immediate results
                status_emoji = {
                    "WORKING": "✅",
                    "RATE_LIMITED": "⏱️",
                    "QUOTA_EXCEEDED": "📊",
                    "INVALID_KEY": "❌",
                    "ERROR": "💥",
                    "TIMEOUT": "⏰",
                    "CONNECTION_ERROR": "🌐"
                }.get(result["status"], "❓")
                
                print(f"Key #{result['index']:2d} ({result['key']:13s}): {status_emoji} {result['status']:15s}", end="")
                if result["error"]:
                    print(f" - {result['error']}")
                else:
                    print()
        
        return results
    
    def print_summary(self, results):
        """Print summary of all results"""
        print("\n" + "=" * 80)
        print("SUMMARY")
        print("=" * 80)
        
        # Count statuses
        status_counts = {}
        for result in results:
            status = result["status"]
            status_counts[status] = status_counts.get(status, 0) + 1
        
        total = len(results)
        
        print(f"Total Keys: {total}")
        print(f"✅ Working: {status_counts.get('WORKING', 0)}")
        print(f"⏱️ Rate Limited: {status_counts.get('RATE_LIMITED', 0)}")
        print(f"📊 Quota Exceeded: {status_counts.get('QUOTA_EXCEEDED', 0)}")
        print(f"❌ Invalid Keys: {status_counts.get('INVALID_KEY', 0)}")
        print(f"💥 Errors: {status_counts.get('ERROR', 0)}")
        print(f"⏰ Timeouts: {status_counts.get('TIMEOUT', 0)}")
        print(f"🌐 Connection Errors: {status_counts.get('CONNECTION_ERROR', 0)}")
        
        # Show good keys
        working_keys = [r for r in results if r["status"] == "WORKING"]
        if working_keys:
            print(f"\n✅ Working Keys:")
            for key in working_keys[:10]:  # Show first 10
                print(f"  #{key['index']} - {key['key']}")
            if len(working_keys) > 10:
                print(f"  ... and {len(working_keys) - 10} more")
        
        # Show problematic keys
        problem_keys = [r for r in results if r["status"] != "WORKING"]
        if problem_keys:
            print(f"\n❌ Problem Keys:")
            for key in problem_keys[:5]:  # Show first 5
                print(f"  #{key['index']} ({key['key']}) - {key['status']}: {key['error']}")
            if len(problem_keys) > 5:
                print(f"  ... and {len(problem_keys) - 5} more issues")
    
    def save_results(self, results):
        """Save results to a JSON file"""
        filename = f"api_key_results_{int(time.time())}.json"
        
        # Add full API keys for reference (be careful with this file!)
        full_results = []
        for result in results:
            full_result = result.copy()
            full_result["full_api_key"] = self.api_keys[result["index"]]
            full_results.append(full_result)
        
        with open(filename, 'w') as f:
            json.dump(full_results, f, indent=2)
        
        print(f"\n💾 Results saved to: {filename}")

def main():
    print("🔑 Simple API Key Health Checker")
    print("=" * 50)
    
    checker = SimpleAPIKeyChecker()
    
    start_time = time.time()
    results = checker.check_all_keys()
    end_time = time.time()
    
    checker.print_summary(results)
    print(f"\n⏱️ Total time: {end_time - start_time:.2f} seconds")
    
    # Auto-save results
    checker.save_results(results)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted by user. Goodbye!")
    except Exception as e:
        print(f"\n💥 Error: {e}")
        sys.exit(1)
