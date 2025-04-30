describe('Test Base', () => {
  it('visit Login', () => {
    cy.visit('/user-sessions/login')
    cy.url().should('include', '/login')
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
    cy.get('#doLogin').click()
    cy.url().should('include', '/home')

    cy.get('.menu-toggle').click()
    cy.get('.btn-logout').click()
    cy.url().should('include', '/user-sessions/login')
  })
})
