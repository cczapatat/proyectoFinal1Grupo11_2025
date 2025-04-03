describe('My First Test', () => {
  it('Visits the initial project page', () => {
    cy.visit('/user-sessions/login')
    cy.contains('Sign Up As Seller')
  })
})

describe('Login Test', () => {
  beforeEach(() => {
    cy.visit('/user-sessions/login')
  })
  it('Show Login View', () => {
    cy.url().should('include', '/user-sessions/login')
  })
  it('Fill login form', () => {
    cy.get('#email').type('admin.admin@sta.com')
    cy.get('#password').type('123456')
    cy.get('.btn-info').click()
    cy.contains('Login successful as ADMIN')
  })
})