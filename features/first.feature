Feature: First feature

  @fail_test @test01
  Scenario: Check stock list
     Given i get stock list
      Then products should can have a valid information

  @success_test @test02
  Scenario: Check information type from stock list
     Given i get stock list
      Then products should can have a valid type information

  @success_test @test03
  Scenario: Update product price
     Given i update product "CMIN3" price
     Given i get stock list
      Then price should be updated