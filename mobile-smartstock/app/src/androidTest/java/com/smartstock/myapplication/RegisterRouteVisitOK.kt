package com.smartstock.myapplication


import android.view.View
import android.view.ViewGroup
import androidx.recyclerview.widget.RecyclerView.ViewHolder
import androidx.test.espresso.Espresso.onView
import androidx.test.espresso.action.ViewActions.*
import androidx.test.espresso.assertion.ViewAssertions.*
import androidx.test.espresso.contrib.RecyclerViewActions.actionOnItemAtPosition
import androidx.test.espresso.matcher.ViewMatchers.*
import androidx.test.ext.junit.rules.ActivityScenarioRule
import androidx.test.ext.junit.runners.AndroidJUnit4
import androidx.test.filters.LargeTest
import org.hamcrest.Description
import org.hamcrest.Matcher
import org.hamcrest.Matchers.allOf
import org.hamcrest.Matchers.`is`
import org.hamcrest.TypeSafeMatcher
import org.junit.Rule
import org.junit.Test
import org.junit.runner.RunWith

@LargeTest
@RunWith(AndroidJUnit4::class)
class RegisterRouteVisitOK {

    @Rule
    @JvmField
    var mActivityScenarioRule = ActivityScenarioRule(SplashActivity::class.java)

    @Test
    fun registerRouteVisitOK() {
        val textInputEditText = onView(
            allOf(
                withId(R.id.email),
                childAtPosition(
                    childAtPosition(
                        withId(R.id.textField5),
                        0
                    ),
                    0
                ),
                isDisplayed()
            )
        )
        textInputEditText.perform(replaceText("seller@seller.com"), closeSoftKeyboard())

        val textInputEditText2 = onView(
            allOf(
                withId(R.id.password),
                childAtPosition(
                    childAtPosition(
                        withId(R.id.textField6),
                        0
                    ),
                    0
                ),
                isDisplayed()
            )
        )
        textInputEditText2.perform(replaceText("123456"), closeSoftKeyboard())

        val textInputEditText3 = onView(
            allOf(
                withId(R.id.password), withText("123456"),
                childAtPosition(
                    childAtPosition(
                        withId(R.id.textField6),
                        0
                    ),
                    0
                ),
                isDisplayed()
            )
        )
        textInputEditText3.perform(pressImeActionButton())

        val materialButton = onView(
            allOf(
                withId(R.id.buttonLogin), withText("Signin"),
                childAtPosition(
                    allOf(
                        withId(R.id.section_11),
                        childAtPosition(
                            withId(R.id.logintest),
                            5
                        )
                    ),
                    0
                ),
                isDisplayed()
            )
        )
        materialButton.perform(click())

        val bottomNavigationItemView = onView(
            allOf(
                withId(R.id.nav_menu), withContentDescription("Menu"),
                childAtPosition(
                    childAtPosition(
                        withId(R.id.bottom_navigation),
                        0
                    ),
                    1
                ),
                isDisplayed()
            )
        )
        bottomNavigationItemView.perform(click())

        val materialTextView = onView(
            allOf(
                withId(android.R.id.title), withText("Visit registration"),
                childAtPosition(
                    childAtPosition(
                        withId(android.R.id.content),
                        0
                    ),
                    0
                ),
                isDisplayed()
            )
        )
        materialTextView.perform(click())

        val checkableImageButton = onView(
            allOf(
                withId(com.google.android.material.R.id.text_input_end_icon),
                withContentDescription("Show dropdown menu"),
                childAtPosition(
                    childAtPosition(
                        withClassName(`is`("com.google.android.material.textfield.EndCompoundLayout")),
                        1
                    ),
                    0
                ),
                isDisplayed()
            )
        )
        checkableImageButton.perform(click())


        val textInputEditText4 = onView(
            allOf(
                withId(R.id.longDescriptionField),
                childAtPosition(
                    childAtPosition(
                        withId(R.id.descriptionLongTextFieldLabel),
                        0
                    ),
                    0
                ),
                isDisplayed()
            )
        )
        textInputEditText4.perform(replaceText("This is a test"), closeSoftKeyboard())

        val materialButton2 = onView(
            allOf(
                withId(R.id.buttonAddProduct), withText("Add product"),
                childAtPosition(
                    allOf(
                        withId(R.id.section_create_route_visit_4),
                        childAtPosition(
                            withId(R.id.routes_create_visit),
                            3
                        )
                    ),
                    0
                ),
                isDisplayed()
            )
        )
        materialButton2.perform(click())

        val recyclerView = onView(
            allOf(
                withId(R.id.simpleProductRecyclerView),
                childAtPosition(
                    withId(R.id.add_producto_section_2),
                    0
                )
            )
        )
        recyclerView.perform(actionOnItemAtPosition<ViewHolder>(0, click()))

        val materialButton3 = onView(
            allOf(
                withId(android.R.id.button1), withText("Accept"),
                childAtPosition(
                    childAtPosition(
                        withId(androidx.appcompat.R.id.buttonPanel),
                        0
                    ),
                    3
                )
            )
        )
        materialButton3.perform(scrollTo(), click())

        val materialButton4 = onView(
            allOf(
                withId(R.id.buttonAcceptCreate), withText("Create"),
                childAtPosition(
                    allOf(
                        withId(R.id.section_create_route_visit_6),
                        childAtPosition(
                            withId(R.id.routes_create_visit),
                            5
                        )
                    ),
                    1
                ),
                isDisplayed()
            )
        )
        materialButton4.perform(click())

        val textView = onView(
            allOf(
                withId(R.id.client_list), withText("My Clients"),
                withParent(
                    allOf(
                        withId(R.id.section_20),
                        withParent(withId(R.id.listremindertest))
                    )
                ),
                isDisplayed()
            )
        )
        textView.check(matches(isDisplayed()))
    }

    private fun childAtPosition(
        parentMatcher: Matcher<View>, position: Int
    ): Matcher<View> {

        return object : TypeSafeMatcher<View>() {
            override fun describeTo(description: Description) {
                description.appendText("Child at position $position in parent ")
                parentMatcher.describeTo(description)
            }

            public override fun matchesSafely(view: View): Boolean {
                val parent = view.parent
                return parent is ViewGroup && parentMatcher.matches(parent)
                        && view == parent.getChildAt(position)
            }
        }
    }
}
