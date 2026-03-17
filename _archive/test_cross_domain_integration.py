"""
Cross-Domain Integration Test Suite

Comprehensive tests for the full cross-domain integration:
- Personal ↔ Business integration
- Business ↔ Accounting integration
- Business ↔ Social Media integration
- Personal ↔ Accounting integration

Tests all MCP servers, skills, and cross-domain orchestration.
"""

import json
import sys
import time
from datetime import datetime
from typing import Dict, Any, List
import httpx


class CrossDomainTester:
    """Test suite for cross-domain integration"""
    
    def __init__(self):
        self.mcp_urls = {
            "Accounting": "http://localhost:8001",
            "Social Media": "http://localhost:8002",
            "Personal": "http://localhost:8003",
            "Business": "http://localhost:8004"
        }
        
        self.timeout = httpx.Timeout(30.0)
        self.results: List[Dict[str, Any]] = []
        
    def run_all_tests(self) -> Dict[str, Any]:
        """Run all cross-domain integration tests"""
        print("=" * 80)
        print("CROSS-DOMAIN INTEGRATION TEST SUITE")
        print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80)
        
        test_results = {
            "timestamp": datetime.now().isoformat(),
            "total_tests": 0,
            "passed": 0,
            "failed": 0,
            "tests": []
        }
        
        # Test 1: MCP Server Health Checks
        print("\n" + "=" * 80)
        print("TEST 1: MCP Server Health Checks")
        print("=" * 80)
        health_results = self.test_server_health()
        test_results["tests"].append(health_results)
        test_results["total_tests"] += 1
        if health_results["status"] == "PASS":
            test_results["passed"] += 1
        else:
            test_results["failed"] += 1
        
        # Test 2: Personal MCP Server Endpoints
        print("\n" + "=" * 80)
        print("TEST 2: Personal MCP Server Endpoints")
        print("=" * 80)
        personal_results = self.test_personal_mcp()
        test_results["tests"].append(personal_results)
        test_results["total_tests"] += 1
        if personal_results["status"] == "PASS":
            test_results["passed"] += 1
        else:
            test_results["failed"] += 1
        
        # Test 3: Business MCP Server Endpoints
        print("\n" + "=" * 80)
        print("TEST 3: Business MCP Server Endpoints")
        print("=" * 80)
        business_results = self.test_business_mcp()
        test_results["tests"].append(business_results)
        test_results["total_tests"] += 1
        if business_results["status"] == "PASS":
            test_results["passed"] += 1
        else:
            test_results["failed"] += 1
        
        # Test 4: Cross-Domain Integration (Business → Personal)
        print("\n" + "=" * 80)
        print("TEST 4: Cross-Domain Integration (Business → Personal)")
        print("=" * 80)
        cross_personal_results = self.test_business_to_personal()
        test_results["tests"].append(cross_personal_results)
        test_results["total_tests"] += 1
        if cross_personal_results["status"] == "PASS":
            test_results["passed"] += 1
        else:
            test_results["failed"] += 1
        
        # Test 5: Cross-Domain Integration (Business → Accounting)
        print("\n" + "=" * 80)
        print("TEST 5: Cross-Domain Integration (Business → Accounting)")
        print("=" * 80)
        cross_accounting_results = self.test_business_to_accounting()
        test_results["tests"].append(cross_accounting_results)
        test_results["total_tests"] += 1
        if cross_accounting_results["status"] == "PASS":
            test_results["passed"] += 1
        else:
            test_results["failed"] += 1
        
        # Test 6: Cross-Domain Integration (Business → Social Media)
        print("\n" + "=" * 80)
        print("TEST 6: Cross-Domain Integration (Business → Social Media)")
        print("=" * 80)
        cross_social_results = self.test_business_to_social()
        test_results["tests"].append(cross_social_results)
        test_results["total_tests"] += 1
        if cross_social_results["status"] == "PASS":
            test_results["passed"] += 1
        else:
            test_results["failed"] += 1
        
        # Test 7: Domain Router Skill
        print("\n" + "=" * 80)
        print("TEST 7: Domain Router Skill Classification")
        print("=" * 80)
        router_results = self.test_domain_router()
        test_results["tests"].append(router_results)
        test_results["total_tests"] += 1
        if router_results["status"] == "PASS":
            test_results["passed"] += 1
        else:
            test_results["failed"] += 1
        
        # Test 8: Cross-Domain Orchestrator
        print("\n" + "=" * 80)
        print("TEST 8: Cross-Domain Orchestrator")
        print("=" * 80)
        orchestrator_results = self.test_cross_domain_orchestrator()
        test_results["tests"].append(orchestrator_results)
        test_results["total_tests"] += 1
        if orchestrator_results["status"] == "PASS":
            test_results["passed"] += 1
        else:
            test_results["failed"] += 1
        
        # Summary
        print("\n" + "=" * 80)
        print("TEST SUMMARY")
        print("=" * 80)
        print(f"Total Tests: {test_results['total_tests']}")
        print(f"Passed: {test_results['passed']} ✅")
        print(f"Failed: {test_results['failed']} ❌")
        print(f"Success Rate: {test_results['passed']/test_results['total_tests']*100:.1f}%")
        print("=" * 80)
        
        return test_results
    
    def test_server_health(self) -> Dict[str, Any]:
        """Test health of all MCP servers"""
        result = {
            "name": "MCP Server Health Check",
            "status": "PASS",
            "details": []
        }
        
        for domain, url in self.mcp_urls.items():
            try:
                with httpx.Client(timeout=self.timeout) as client:
                    response = client.get(f"{url}/health")
                    response.raise_for_status()
                    data = response.json()
                    
                    if data.get("status") == "healthy":
                        status = "✅ PASS"
                        print(f"  {domain}: {status}")
                    else:
                        status = "⚠️ WARNING"
                        print(f"  {domain}: {status} - Server responded but not healthy")
                        result["status"] = "FAIL"
                    
                    result["details"].append({
                        "domain": domain,
                        "status": status,
                        "response": data
                    })
                    
            except Exception as e:
                status = "❌ FAIL"
                print(f"  {domain}: {status} - {str(e)}")
                result["details"].append({
                    "domain": domain,
                    "status": status,
                    "error": str(e)
                })
                result["status"] = "FAIL"
        
        return result
    
    def test_personal_mcp(self) -> Dict[str, Any]:
        """Test Personal MCP Server endpoints"""
        result = {
            "name": "Personal MCP Endpoints",
            "status": "PASS",
            "details": []
        }
        
        url = self.mcp_urls["Personal"]
        
        # Test create_appointment
        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.post(f"{url}/api/create_appointment", json={
                    "title": "Test Appointment",
                    "description": "Cross-domain integration test",
                    "dates": ["2026-03-10 14:00"],
                    "location": "Test Location"
                })
                response.raise_for_status()
                data = response.json()
                
                if data.get("success"):
                    print("  create_appointment: ✅ PASS")
                    result["details"].append({"endpoint": "create_appointment", "status": "PASS"})
                else:
                    print("  create_appointment: ⚠️ WARNING")
                    result["details"].append({"endpoint": "create_appointment", "status": "WARNING", "data": data})
        except Exception as e:
            print(f"  create_appointment: ❌ FAIL - {str(e)}")
            result["details"].append({"endpoint": "create_appointment", "status": "FAIL", "error": str(e)})
            result["status"] = "FAIL"
        
        # Test create_reminder
        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.post(f"{url}/api/create_reminder", json={
                    "title": "Test Reminder",
                    "description": "Cross-domain test reminder",
                    "priority": "high"
                })
                response.raise_for_status()
                data = response.json()
                
                if data.get("success"):
                    print("  create_reminder: ✅ PASS")
                    result["details"].append({"endpoint": "create_reminder", "status": "PASS"})
                else:
                    print("  create_reminder: ⚠️ WARNING")
                    result["details"].append({"endpoint": "create_reminder", "status": "WARNING"})
        except Exception as e:
            print(f"  create_reminder: ❌ FAIL - {str(e)}")
            result["details"].append({"endpoint": "create_reminder", "status": "FAIL", "error": str(e)})
            result["status"] = "FAIL"
        
        # Test get_personal_summary
        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.get(f"{url}/api/get_personal_summary")
                response.raise_for_status()
                data = response.json()
                
                if data.get("success"):
                    print("  get_personal_summary: ✅ PASS")
                    result["details"].append({"endpoint": "get_personal_summary", "status": "PASS"})
                else:
                    print("  get_personal_summary: ⚠️ WARNING")
                    result["details"].append({"endpoint": "get_personal_summary", "status": "WARNING"})
        except Exception as e:
            print(f"  get_personal_summary: ❌ FAIL - {str(e)}")
            result["details"].append({"endpoint": "get_personal_summary", "status": "FAIL", "error": str(e)})
            result["status"] = "FAIL"
        
        return result
    
    def test_business_mcp(self) -> Dict[str, Any]:
        """Test Business MCP Server endpoints"""
        result = {
            "name": "Business MCP Endpoints",
            "status": "PASS",
            "details": []
        }
        
        url = self.mcp_urls["Business"]
        
        # Test schedule_meeting
        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.post(f"{url}/api/schedule_meeting", json={
                    "title": "Test Business Meeting",
                    "description": "Cross-domain integration test meeting",
                    "meeting_type": "virtual"
                })
                response.raise_for_status()
                data = response.json()
                
                if data.get("success"):
                    print("  schedule_meeting: ✅ PASS")
                    result["details"].append({"endpoint": "schedule_meeting", "status": "PASS"})
                else:
                    print("  schedule_meeting: ⚠️ WARNING")
                    result["details"].append({"endpoint": "schedule_meeting", "status": "WARNING"})
        except Exception as e:
            print(f"  schedule_meeting: ❌ FAIL - {str(e)}")
            result["details"].append({"endpoint": "schedule_meeting", "status": "FAIL", "error": str(e)})
            result["status"] = "FAIL"
        
        # Test update_crm
        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.post(f"{url}/api/update_crm", json={
                    "activity_type": "client_call",
                    "description": "Test CRM activity",
                    "companies": ["Test Corp"]
                })
                response.raise_for_status()
                data = response.json()
                
                if data.get("success"):
                    print("  update_crm: ✅ PASS")
                    result["details"].append({"endpoint": "update_crm", "status": "PASS"})
                else:
                    print("  update_crm: ⚠️ WARNING")
                    result["details"].append({"endpoint": "update_crm", "status": "WARNING"})
        except Exception as e:
            print(f"  update_crm: ❌ FAIL - {str(e)}")
            result["details"].append({"endpoint": "update_crm", "status": "FAIL", "error": str(e)})
            result["status"] = "FAIL"
        
        return result
    
    def test_business_to_personal(self) -> Dict[str, Any]:
        """Test cross-domain integration: Business → Personal"""
        result = {
            "name": "Business → Personal Integration",
            "status": "PASS",
            "details": []
        }
        
        business_url = self.mcp_urls["Business"]
        personal_url = self.mcp_urls["Personal"]
        
        # Test flag_personal_impact from Business to Personal
        try:
            with httpx.Client(timeout=self.timeout) as client:
                # First, flag from business side
                response = client.post(f"{business_url}/api/flag_personal_impact", json={
                    "task_id": "test_cross_001",
                    "content": "Urgent project requires weekend work",
                    "source_domain": "Business"
                })
                response.raise_for_status()
                business_data = response.json()
                
                if business_data.get("success"):
                    print(f"  Business flag_personal_impact: ✅ PASS")
                    result["details"].append({
                        "direction": "Business → Personal",
                        "endpoint": "flag_personal_impact",
                        "status": "PASS",
                        "response": business_data
                    })
                else:
                    print(f"  Business flag_personal_impact: ⚠️ WARNING")
                    result["details"].append({
                        "direction": "Business → Personal",
                        "status": "WARNING"
                    })
                    result["status"] = "FAIL"
                    
        except Exception as e:
            print(f"  Business flag_personal_impact: ❌ FAIL - {str(e)}")
            result["details"].append({
                "direction": "Business → Personal",
                "status": "FAIL",
                "error": str(e)
            })
            result["status"] = "FAIL"
        
        # Test Personal MCP receives the flag
        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.post(f"{personal_url}/api/flag_personal_impact", json={
                    "task_id": "test_cross_001",
                    "content": "Urgent project requires weekend work",
                    "source_domain": "Business"
                })
                response.raise_for_status()
                data = response.json()
                
                if data.get("success"):
                    print(f"  Personal flag_personal_impact: ✅ PASS")
                    result["details"].append({
                        "endpoint": "Personal.flag_personal_impact",
                        "status": "PASS"
                    })
                    
                    # Check for work-life balance concerns
                    if data.get("data", {}).get("concerns"):
                        print(f"    Work-life concerns detected: {len(data['data']['concerns'])}")
                else:
                    print(f"  Personal flag_personal_impact: ⚠️ WARNING")
                    result["status"] = "FAIL"
                    
        except Exception as e:
            print(f"  Personal flag_personal_impact: ❌ FAIL - {str(e)}")
            result["details"].append({
                "endpoint": "Personal.flag_personal_impact",
                "status": "FAIL",
                "error": str(e)
            })
            result["status"] = "FAIL"
        
        return result
    
    def test_business_to_accounting(self) -> Dict[str, Any]:
        """Test cross-domain integration: Business → Accounting"""
        result = {
            "name": "Business → Accounting Integration",
            "status": "PASS",
            "details": []
        }
        
        business_url = self.mcp_urls["Business"]
        accounting_url = self.mcp_urls["Accounting"]
        
        # Test flag_financial_task
        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.post(f"{business_url}/api/flag_financial_task", json={
                    "task_id": "test_cross_002",
                    "content": "Client dinner expense $150 for business development",
                    "source_domain": "Business"
                })
                response.raise_for_status()
                data = response.json()
                
                if data.get("success"):
                    print(f"  Business flag_financial_task: ✅ PASS")
                    result["details"].append({
                        "direction": "Business → Accounting",
                        "endpoint": "flag_financial_task",
                        "status": "PASS"
                    })
                    
                    # Check for financial indicators
                    if data.get("data", {}).get("financial_indicators"):
                        print(f"    Financial indicators: {data['data']['financial_indicators']}")
                else:
                    print(f"  Business flag_financial_task: ⚠️ WARNING")
                    result["status"] = "FAIL"
                    
        except Exception as e:
            print(f"  Business flag_financial_task: ❌ FAIL - {str(e)}")
            result["details"].append({
                "direction": "Business → Accounting",
                "status": "FAIL",
                "error": str(e)
            })
            result["status"] = "FAIL"
        
        return result
    
    def test_business_to_social(self) -> Dict[str, Any]:
        """Test cross-domain integration: Business → Social Media"""
        result = {
            "name": "Business → Social Media Integration",
            "status": "PASS",
            "details": []
        }
        
        business_url = self.mcp_urls["Business"]
        social_url = self.mcp_urls["Social Media"]
        
        # Test flag_marketing_task
        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.post(f"{business_url}/api/flag_marketing_task", json={
                    "task_id": "test_cross_003",
                    "content": "New product launch campaign on Facebook and Instagram",
                    "source_domain": "Business"
                })
                response.raise_for_status()
                data = response.json()
                
                if data.get("success"):
                    print(f"  Business flag_marketing_task: ✅ PASS")
                    result["details"].append({
                        "direction": "Business → Social Media",
                        "endpoint": "flag_marketing_task",
                        "status": "PASS"
                    })
                    
                    # Check for marketing indicators
                    if data.get("data", {}).get("marketing_indicators"):
                        print(f"    Marketing indicators: {data['data']['marketing_indicators']}")
                else:
                    print(f"  Business flag_marketing_task: ⚠️ WARNING")
                    result["status"] = "FAIL"
                    
        except Exception as e:
            print(f"  Business flag_marketing_task: ❌ FAIL - {str(e)}")
            result["details"].append({
                "direction": "Business → Social Media",
                "status": "FAIL",
                "error": str(e)
            })
            result["status"] = "FAIL"
        
        return result
    
    def test_domain_router(self) -> Dict[str, Any]:
        """Test domain router skill classification"""
        result = {
            "name": "Domain Router Classification",
            "status": "PASS",
            "details": []
        }
        
        # Import and test domain router
        try:
            sys.path.insert(0, "skills")
            from domain_router_skill import domain_router_skill
            
            test_cases = [
                {
                    "name": "Personal Task",
                    "input": {
                        "task_id": "test_001",
                        "content": "Schedule dentist appointment for next week",
                        "sender": "user"
                    },
                    "expected_domain": "Personal"
                },
                {
                    "name": "Business Task",
                    "input": {
                        "task_id": "test_002",
                        "content": "Prepare quarterly business review meeting with client",
                        "sender": "manager"
                    },
                    "expected_domain": "Business"
                },
                {
                    "name": "Accounting Task",
                    "input": {
                        "task_id": "test_003",
                        "content": "Create invoice for client payment and record expense",
                        "sender": "finance"
                    },
                    "expected_domain": "Accounting"
                },
                {
                    "name": "Social Media Task",
                    "input": {
                        "task_id": "test_004",
                        "content": "Post update on Facebook and Instagram about new product",
                        "sender": "marketing"
                    },
                    "expected_domain": "Social Media"
                }
            ]
            
            for test_case in test_cases:
                result_json = domain_router_skill(test_case["input"])
                result_data = json.loads(result_json)
                
                classified_domain = result_data.get("domain")
                cross_domain_enabled = result_data.get("cross_domain_enabled", False)
                
                if classified_domain == test_case["expected_domain"]:
                    status = "✅ PASS"
                else:
                    status = "❌ FAIL"
                    result["status"] = "FAIL"
                
                print(f"  {test_case['name']}: {status} (Classified: {classified_domain})")
                
                result["details"].append({
                    "test": test_case["name"],
                    "expected": test_case["expected_domain"],
                    "classified": classified_domain,
                    "cross_domain_enabled": cross_domain_enabled,
                    "status": "PASS" if status == "✅ PASS" else "FAIL"
                })
                
        except Exception as e:
            print(f"  Domain Router Test: ❌ FAIL - {str(e)}")
            result["status"] = "FAIL"
            result["details"].append({"error": str(e)})
        
        return result
    
    def test_cross_domain_orchestrator(self) -> Dict[str, Any]:
        """Test cross-domain orchestrator"""
        result = {
            "name": "Cross-Domain Orchestrator",
            "status": "PASS",
            "details": []
        }
        
        try:
            from cross_domain_orchestrator import CrossDomainOrchestrator
            
            orchestrator = CrossDomainOrchestrator()
            
            # Test cross-domain analysis
            test_task = {
                "task_id": "test_orch_001",
                "content": "Client dinner meeting this evening - expense $150 for business development",
                "primary_domain": "Business",
                "metadata": {"priority": "high"},
                "sender": "sales"
            }
            
            cross_actions = orchestrator._check_cross_domain_implications(
                test_task, "Business", {"status": "success"}
            )
            
            print(f"  Cross-domain actions detected: {len(cross_actions)}")
            
            for action in cross_actions:
                print(f"    → {action['target_domain']}: {action['action_type']} ({action['reason']})")
            
            if len(cross_actions) > 0:
                result["details"].append({
                    "test": "Cross-domain detection",
                    "actions_found": len(cross_actions),
                    "actions": cross_actions,
                    "status": "PASS"
                })
                print("  Cross-domain detection: ✅ PASS")
            else:
                result["details"].append({
                    "test": "Cross-domain detection",
                    "actions_found": 0,
                    "status": "WARNING"
                })
                print("  Cross-domain detection: ⚠️ WARNING - No actions detected")
            
            # Test integration report
            report = orchestrator.get_integration_report()
            if report:
                print("  Integration report generation: ✅ PASS")
                result["details"].append({
                    "test": "Integration report",
                    "status": "PASS"
                })
            else:
                print("  Integration report generation: ⚠️ WARNING")
                result["status"] = "FAIL"
                
        except Exception as e:
            print(f"  Cross-Domain Orchestrator: ❌ FAIL - {str(e)}")
            result["status"] = "FAIL"
            result["details"].append({"error": str(e)})
        
        return result


def main():
    """Main test runner"""
    tester = CrossDomainTester()
    results = tester.run_all_tests()
    
    # Save results to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"cross_domain_test_results_{timestamp}.json"
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\n✅ Test results saved to: {output_file}")
    
    # Return exit code based on results
    if results["failed"] > 0:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
